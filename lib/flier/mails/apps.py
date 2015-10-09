from django.apps import AppConfig as DjangoAppConfig
from django.utils.translation import (
    ugettext_lazy as _,
)


class AppConfig(DjangoAppConfig):
    name = 'mails'
    verbose_name = _("Flier Mails")

    def ready(self):
        import tasks        # NOQA
