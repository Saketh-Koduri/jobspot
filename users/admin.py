from django.contrib import admin
from users.models import CustomUser
# Register your models here.

from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'is_company', 'is_seeker', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_company', 'is_seeker')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
