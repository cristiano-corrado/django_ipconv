from django.contrib import admin
from .models import IPUnpacked
from .models import IPChaos

@admin.register(IPUnpacked)

class IPBoardAdmin(admin.ModelAdmin):
    date_heirarchy = (
        'modified',
    )

    list_display = (
        'ipunpack',


    )

@admin.register(IPChaos)
class IPBoardAdmin(admin.ModelAdmin):
    date_heirarchy = (
        'modified',
    )

    list_display = (
        'string',
        'type'

    )
