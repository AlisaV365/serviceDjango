from django.contrib import admin

from users.models import User


@admin.register(User)
class ClientAdmin(admin.ModelAdmin):
    """Регистрация модели Client в админ-панели"""
    list_display = ['email', 'first_name', 'last_name', 'comment']