from django.contrib import admin
from django.apps import apps
from django import forms, template
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe as _S
from django.core.urlresolvers import reverse

import models


def _T(src, **ctx):
    return _S(template.Template(src).render(template.Context(ctx)))


def change_link(model):
    return reverse("admin:{0}_{1}_change".format(
        model._meta.app_label,
        model._meta.model_name,
    ), args=[model.id])


def changelist_link(model, parent=None):
    url = reverse("admin:{0}_{1}_changelist".format(
        model._meta.app_label,
        model._meta.model_name,
    ))
    if parent:
        r = [i.field.name for i in parent._meta.related_objects
             if i.related_model == model]
        if len(r) > 0:
            url += "?{0}={1}".format(r[0], parent.id)
    # finally returns url
    return url


class AddressAdminForm(forms.ModelForm):
    class Meta:
        model = models.Address
        exclude = ['domain', ]


class AddressAdmin(admin.ModelAdmin):
    list_excludes = ('created_at', )
    form = AddressAdminForm
    search_fields = ('address', 'domain', )
    list_filter = ('enabled', )


class SenderAdmin(admin.ModelAdmin):
    list_excludes = ('created_at', )
    list_additionals = ('instance_object', )
    list_filter = ('enabled', )
    search_fields = ('address', )
    readonly_fields = ('instance_object', )

    def instance_object(self, obj):
        link = change_link(obj.instance)
        return _T('''<a href="{{ u }}">{{ m }}</a>''', u=link, m=obj.instance)

    instance_object.short_description = _("Instance Object")
    instance_object.allow_tags = True


class RecipientAdmin(admin.ModelAdmin):
    list_filter = ('status', )
    list_excludes = (
        'created_at', 'message', 'content_type', 'object_id',
        'target_content_type', 'target_object_id',
    )
    list_additionals = ('content_object', 'target_object', )
    date_hierarchy = 'sent_at'
    raw_id_fields = ('sender', 'to', )
    readonly_fields = (
        'content_object', 'target_object', 'message_view', )
    exclude = [
        'content_type', 'object_id',
        'target_content_type', 'target_object_id', ]
    search_fields = ('to__address', 'key', 'sender__address', )

    def get_fieldsets(self, request, obj=None):
        res = super(RecipientAdmin, self).get_fieldsets(request, obj=obj)
        if obj is None:
            ex = ['key', 'message_id', 'sent_at', 'status', 'message']
        else:
            ex = ['message', ]
        res = [
            (r[0], {'fields': [i for i in r[1]['fields'] if i not in ex]})
            for r in res
        ]
        return res

    def message_view(self, obj):
        return _T('''<hr><pre>{{ m }}</pre>''', m=obj.message)

    message_view.short_description = _("Message to Recipient")
    message_view.allow_tags = True

    def content_object(self, obj):
        if not obj.content_object:
            return
        url = change_link(obj.content_object)

        return _T(
            '''<a href="{{u}}">{{o}}</a>''', u=url,
            id=obj.object_id, o=obj.content_object)

    content_object.short_description = _("Content Object")
    content_object.allow_tags = True

    def target_object(self, obj):
        if not obj.target_object:
            return

        name = "admin:{}_{}_change".format(
            obj.target_content_type.app_label,
            obj.target_content_type.model,)

        return _T(
            '''<a href="{% url name id %}">{{o}}</a>''',
            name=name, id=obj.target_object_id, o=obj.target_object)

    target_object.short_description = _("Target Object")
    target_object.allow_tags = True


def register(app_fullname, admins, ignore_models=[]):
    app_label = app_fullname.split('.')[-2:][0]
    for n, model in apps.get_app_config(app_label).models.items():
        if model.__name__ in ignore_models:
            continue
        name = "%sAdmin" % model.__name__
        admin_class = admins.get(name, None)
        if admin_class is None:
            admin_class = type(
                "%sAdmin" % model.__name__,
                (admin.ModelAdmin,), {},
            )

        if admin_class.list_display == ('__str__',):
            excludes = getattr(admin_class, 'list_excludes', ())
            additionals = getattr(admin_class, 'list_additionals', ())
            admin_class.list_display = tuple(
                [f.name for f in model._meta.fields
                 if f.name not in excludes]) + additionals

        admin.site.register(model, admin_class)


register(__name__, globals())
