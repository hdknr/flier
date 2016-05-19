from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from flier.admin import register, _T


class ForwarderAdmin(admin.ModelAdmin):
    list_excludes = ('created_at', )
    raw_id_fields = ('forward', )
    list_filter = ('domain', 'deleted', )
    date_hierarchy = 'updated_at'
    search_fields = ('address', 'forward__address', )


class RelayAdmin(admin.ModelAdmin):
    list_excludes = ('created_at', )
    raw_id_fields = ('forwarder', 'sender', )


class MessageAdmin(admin.ModelAdmin):
    list_excludes = ('created_at', 'raw_message', )
    list_filter = ('domain', )
    raw_id_fields = ('relay', )
    date_hierarchy = 'updated_at'
    search_fields = ('recipient', 'sender', )
    exclude = ('raw_message', )
    readonly_fields = ('raw_message_text', )

    def raw_message_text(self, obj):
        return _T('''<hr><pre>{{ m }}</pre>''', m=obj.raw_message)

    raw_message_text.short_description = _("Message to Recipient")
    raw_message_text.allow_tags = True


class DomainAdmin(admin.ModelAdmin):
    list_filter = ('domain', 'transport', )


class SenderAdmin(admin.ModelAdmin):
    list_filter = ('enabled', 'domain', )

register(__name__, globals())
