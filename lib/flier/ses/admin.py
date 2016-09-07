from django.contrib import admin
from django import template
from django import forms
from django.utils.translation import ugettext_lazy as _
from flier.admin import register
from .models import Source
import json
import models


class TopicAdminInline(admin.TabularInline):
    model = models.Topic
    max_num = 3


class SourceAdminForm(forms.ModelForm):
    force_verify = forms.BooleanField(
        label=_('Verify Email Address'), required=False)

    class Meta:
        model = Source
        exclude = []


class SourceAdmin(admin.ModelAdmin):
    list_excludes = ('created_at', )
    list_filter = ('service', )
    inlines = [TopicAdminInline, ]
    form = SourceAdminForm

    def save_model(self, request, obj, form, change):
        super(SourceAdmin, self).save_model(
            request, obj, form, change)
        if form.cleaned_data.get('force_verify', False):
            form.instance.verify_address()


class NotificationAdmin(admin.ModelAdmin):
    list_excludes = ('created_at', 'headers', )
    list_filter = ('topic', )
    readonly_fields = ('sns_json', 'ses_json', 'headers_json', )

    def sns_json(self, obj):
        return template.Template('''
<pre>
{{ m }}
</pre>
''',).render(template.Context(dict(m=obj.message_object.format())))

    sns_json.short_description = _('SNS Message')
    sns_json.allow_tags = True

    def headers_json(self, obj):
        m = json.dumps(obj.headers_object, indent=2)
        return template.Template('''
<pre>
{{ m }}
</pre>
''',).render(template.Context(dict(m=m)))

    headers_json.short_description = _('SNS Headers')
    headers_json.allow_tags = True

    def ses_json(self, obj):
        return template.Template('''
<pre>
{{ m }}
</pre>
''',).render(template.Context(dict(m=obj.message_object.Message.format())))

    ses_json.short_description = _('SES Message')
    ses_json.allow_tags = True

register(__name__, globals())
