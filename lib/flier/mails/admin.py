from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from flier.admin import register
from flier.utils import render


class MailAdmin(admin.ModelAdmin):
    list_filter = ('status', )
    list_excludes = ('body', 'html', )
    list_additionals = ('instance_link', )
    readonly_fields = ('instance_link', )
    raw_id_fields = ('sender', )

    def instance_link(self, obj):
        p = dict(
            id=obj.instance.id, a=obj.instance._meta.app_label,
            m=obj.instance._meta.model_name)
        p['u'] = "admin:{a}_{m}_change".format(**p)

        return render(u'''
        <a href="{% url u id %}">{{a}}.{{m}}</a>
        ''', **p)

    instance_link.short_description = _('Concret Instance')


class MailTemplateAdmin(admin.ModelAdmin):
    list_excludes = ('body', 'html', )


register(__name__, globals())
