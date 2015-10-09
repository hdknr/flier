from django.apps import AppConfig as DjangoAppConfig
from django.utils.translation import (
    ugettext_lazy as _,
)


class AppConfig(DjangoAppConfig):
    name = 'smtp'
    verbose_name = _("Flier SMTP")
