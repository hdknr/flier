from django.core.mail.message import EmailMultiAlternatives
import backends
import uuid


class Domain(object):
    '''Domain:
    '''
    def __unicode__(self):
        return self.domain

    def create_alias_domain(self, name):
        domain, created = self.objects.get_or_create(
            doamin=name, transport='error',
            alias=self)
        return domain

    def add_alias_address(self, user, alias_user=None):
        if not self.alias_domain:
            return
        src = '{0}@{1}'.format(user, self.domain)
        dst = '{0}@{1}'.format(alias_user or user, self.alias_domain.domain)
        alias = self.alias_set.filter(recipient=src).first()
        if alias:
            alias.forward = dst
            alias.save()
        else:
            alias = self.alias_set.create(recipient=src, forward=dst)
        return alias


class Alias(object):
    pass


class Sender(object):
    def verp(self):
        return uuid.uuid1().hex + "." + self.address

    @property
    def backend(self):
        return backends.SmtpBackend()

    @property
    def instance(self):
        return self

    def create_message(self, *args, **kwargs):
        kwargs['from_email'] = self.verp()
        headers = kwargs.get('headers', {})
        headers['From'] = self.address
        kwargs['headers'] = headers
        EmailMultiAlternatives.encoding = kwargs.get('encoding',  None)
        return EmailMultiAlternatives(
            connection=self.backend,
            *args, **kwargs)
