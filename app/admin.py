from django.contrib import admin

# Register your models here.
from .models import Proyecto, Empleado, EmpleadoProyecto, AFP, Implemento, Factura, Capacitacion, Vehiculo, Pago, PagoEmpleado, PagoInsumoServicio, PagoVehiculo, PagoImplemento

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

@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ('id', 'empleado', 'capacitacion', 'monto', 'estado')
    list_filter = ('estado',)
    search_fields = ('detalle', 'empleado__rut', 'capacitacion__id')

@admin.register(Capacitacion)
class CapacitacionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'institution', 'end_date', 'cert')
    search_fields = ('name', 'institution')
    list_filter = ('institution', 'end_date')

@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ('patent', 'model', 'year', 'status', 'vtype')
    search_fields = ('patent', 'model', 'status', 'vtype')
    list_filter = ('status', 'vtype', 'year')

@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ('id', 'descripcion', 'monto', 'fecha')
    search_fields = ('descripcion',)
    list_filter = ('fecha',)

@admin.register(PagoEmpleado)
class PagoEmpleadoAdmin(admin.ModelAdmin):
    list_display = ('pago', 'empleado', 'afp')
    search_fields = ('empleado__nombre', 'afp__nombre')
    list_filter = ('afp',)

@admin.register(PagoInsumoServicio)
class PagoInsumoServicioAdmin(admin.ModelAdmin):
    list_display = ('pago', 'capacitacion')
    search_fields = ('capacitacion__nombre',)

@admin.register(PagoVehiculo)
class PagoVehiculoAdmin(admin.ModelAdmin):
    list_display = ('pago', 'vehiculo')
    search_fields = ('vehiculo__patent', 'vehiculo__model')

@admin.register(PagoImplemento)
class PagoImplementoAdmin(admin.ModelAdmin):
    list_display = ('pago', 'implemento')
    search_fields = ('implemento__nombre',)