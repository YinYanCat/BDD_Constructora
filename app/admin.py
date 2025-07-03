from django.contrib import admin

# Register your models here.
from .models import Proyecto, Empleado, EmpleadoProyecto, AFP, Implemento

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('rut', 'first_name', 'last_name', 'salary', 'is_active')
    search_fields = ('rut', 'first_name', 'last_name')

@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'budget', 'description', 'is_active')
    search_fields = ('name',)

@admin.register(EmpleadoProyecto)
class EmpleadoProyectoAdmin(admin.ModelAdmin):
    list_display = ('worker', 'proyect', 'position', 'bonus_pay')
    list_filter = ('proyect',)

@admin.register(AFP)
class AFPAdmin(admin.ModelAdmin):
    list_display = ('rut', 'name')
    search_fields = ('rut', 'name')

@admin.register(Implemento)
class ImplementoAdmin(admin.ModelAdmin):
    list_display = ('id', 'itype', 'worker')
    search_fields = ('itype', 'worker__first_name', 'worker__last_name')
    list_filter = ('itype',)