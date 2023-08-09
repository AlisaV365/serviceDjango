from django.contrib import admin

from system.models import MailingMessage, Mailing, Blog


@admin.register(MailingMessage)
class MailingMessageAdmin(admin.ModelAdmin):
    """Регистрация модели MailingMessage в админ-панели"""
    list_display = ['title', 'message']


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    """Регистрация модели Mailing в админ-панели"""
    list_display = ['date_time', 'periodicity', 'message']


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    """Регистрация модели Blog"""
    list_display = ['title', 'description', 'image']