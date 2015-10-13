from django.contrib import admin
from django import forms
from django.utils.translation import ugettext_lazy as _
from flier.admin import register

import models


class RecipientAdminForm(forms.ModelForm):
    class Meta:
        model = models.Recipient
        # exclude = ['key', 'message_id', 'status', 'message', ]
        fields = ['mail', 'to', ]

    def is_valid(self):
        res = super(RecipientAdminForm, self).is_valid()
        if res:
            self.instance.sender = self.cleaned_data['mail'].sender
        return res


class RecipientAdmin(admin.ModelAdmin):
    form = RecipientAdminForm
    raw_id_fields = ['mail', 'to', ]
    actions = ['send_message', ]

    def send_message(self, request, queryset):
        for r in queryset:
            r.send_mail()

    send_message.short_description = _('Send Message')


register(__name__, globals())
