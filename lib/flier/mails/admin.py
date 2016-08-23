from django.contrib import admin
from django import forms
from django.utils.translation import ugettext_lazy as _
from flier.admin import register
from flier.utils import render

import models


class MailAdmin(admin.ModelAdmin):
    list_filter = ('status', )
    list_excludes = ('body', 'html', )
    list_additionals = ('instance_link', )
    readonly_fields = ('instance_link', )

    def instance_link(self, obj):
        p = dict(
            id=obj.instance.id, a=obj.instance._meta.app_label,
            m=obj.instance._meta.model_name)
        p['u'] = "admin:{a}_{m}_change".format(**p)

        return render(u'''
        <a href="{% url u id %}">{{a}}.{{m}}</a>
        ''', **p)

    instance_link.short_description = _('Concret Instance')


class MailRecipientAdminForm(forms.ModelForm):
    class Meta:
        model = models.MailRecipient
        # exclude = ['key', 'message_id', 'status', 'message', ]
        fields = ['mail', 'to', ]

    def is_valid(self):
        res = super(MailRecipientAdminForm, self).is_valid()
        if res:
            self.instance.sender = self.cleaned_data['mail'].sender
        return res


class MailRecipientAdmin(admin.ModelAdmin):
    form = MailRecipientAdminForm
    raw_id_fields = ['mail', 'to', ]
    actions = ['send_message', ]

    def send_message(self, request, queryset):
        for r in queryset:
            r.send_mail()

    send_message.short_description = _('Send Message')


register(__name__, globals())
