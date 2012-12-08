from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Profil

from sorl.thumbnail.admin import AdminImageMixin

class ProfilInline(AdminImageMixin, admin.StackedInline):
    model = Profil
    can_delete = False


class CustomUserAdmin(UserAdmin):
    inlines = UserAdmin.inlines + [ProfilInline]


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
