from django.contrib import admin
from .models import Upload_video


class ActionCamAdmin(admin.ModelAdmin):
    search_fields = ['subject']

admin.site.register(Upload_video, ActionCamAdmin)