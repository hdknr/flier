from django.core.mail.message import EmailMultiAlternatives


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
    def create_message(self, *args, **kwargs):
        from_email = ''         # TODO: return path
        EmailMultiAlternatives.encoding = kwargs.get('enncoding',  None)
        return EmailMultiAlternatives(
            from_email=from_email,       # may be VERP
            *args, **kwargs
        )
