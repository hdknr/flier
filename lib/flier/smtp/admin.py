from django.contrib import admin
from flier.admin import register


class ForwarderAdmin(admin.ModelAdmin):
    list_excludes = ('created_at', )
    raw_id_fields = ('forward', )


class RelayAdmin(admin.ModelAdmin):
    list_excludes = ('created_at', )
    raw_id_fields = ('forwarder', 'sender', )


class MessageAdmin(admin.ModelAdmin):
    list_excludes = ('created_at', )
    raw_id_fields = ('relay', )


register(__name__, globals())
