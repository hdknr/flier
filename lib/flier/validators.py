from __future__ import unicode_literals
'''
http://emailregex.com/

::

    r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
'''
import re
from django.core.validators import EmailValidator, _lazy_re_compile
from django.utils.deconstruct import deconstructible
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _


@deconstructible
class EmailValidatorEx(EmailValidator):
    user_regex = _lazy_re_compile(r"(^[a-zA-Z0-9_.+-]+)", re.IGNORECASE)
    domain_regex = _lazy_re_compile(
        r"([a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", re.IGNORECASE)

    def check(self, value):
        value = force_text(value)

        if not value:
            return False, _('No Value')

        if '@' not in value:
            return False, _('{}:No @ mark').format(value)

        user_part, domain_part = value.rsplit('@', 1)

        if not self.user_regex.match(user_part):
            return False, _('{}:Wrong User Part').format(user_part)

        if domain_part in self.domain_whitelist:
            return True, ''

        if self.validate_domain_part(domain_part):
            return True, ''

        # Try for possible IDN domain-part
        try:
            domain_part = domain_part.encode('idna').decode('ascii')
            if self.validate_domain_part(domain_part):
                return True, ''
        except UnicodeError:
            pass

        return False, _('{}:Wrong Domain Part').format(domain_part)

# no exception is raised when call validate_email(addr), and OK
validate_email = EmailValidatorEx()
