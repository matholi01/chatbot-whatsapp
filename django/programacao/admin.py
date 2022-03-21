from django.contrib import admin
from .models import Evento, Igreja, Administrador
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

# Register your models here.
admin.site.register(Igreja) 

# Define an inline admin descriptor for Administrador model
# which acts a bit like a singleton
class AdministradorInline(admin.TabularInline):
    model = Administrador
    can_delete = False
    verbose_name_plural = 'Administrador'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (AdministradorInline,) 

@admin.register(Evento)
class Evento(admin.ModelAdmin):

    # Filtra os eventos mostrados na página do admin do django
    def get_queryset(self, request):
        qs = super(Evento,self).get_queryset(request)
        # Se o usuário logado for um superusuário, retornamos todos os eventos cadastrados
        if request.user.is_superuser:
            return qs
        # Caso não seja, retornamos apenas os eventos da igreja dele
        return qs.filter(igreja__nome=request.user.administrador.igreja.nome) 

    # Se o usuário logado não for um superusuário, não mostramos o campo igreja,
    # pois ele pode criar apenas eventos da igreja dele
    def get_exclude(self, request, obj):
        if not request.user.is_superuser:
            return ['igreja',]

    # Se o usuário logado não for um superusuário, salvamos o evento automaticamente sendo da igreja dele.
    # Apenas superusuários podem criar eventos de qualquer igreja cadastrada no banco de dados
    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.igreja = request.user.administrador.igreja 
        super().save_model(request, obj, form, change)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

