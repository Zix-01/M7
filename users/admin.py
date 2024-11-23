from django.contrib import admin
from users.models import User, Payments


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['pk', 'email', 'is_active', 'is_staff', 'is_superuser']


@admin.register(Payments)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['pk']
