from django.contrib import admin
from .models import Evento, Igreja, Administrador
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

# Register your models here.

admin.site.register(Evento)
admin.site.register(Igreja)

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class AdministradorInline(admin.StackedInline):
    model = Administrador
    can_delete = False
    verbose_name_plural = 'Administrador'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (AdministradorInline,)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

