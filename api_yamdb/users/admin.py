from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import UserProfile

UserAdmin.fieldsets += (
    (_('Extra Fields'), {'fields': ('bio', 'role',)}),
)

admin.site.register(UserProfile, UserAdmin)
