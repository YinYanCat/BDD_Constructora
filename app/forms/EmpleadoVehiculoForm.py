from django import forms
from app.models import Empleado, Vehiculo, AsignacionVehiculo

class EmpleadoVehiculoForm(forms.Form):
    worker = forms.ModelChoiceField(queryset=Empleado.objects.none(), required=True, label='Empleado')

    def __init__(self, vehiculo=None, *args, **kwargs):
        super().__init__(*args,**kwargs)
        if vehiculo:
            empleados_activos = Empleado.objects.filter(is_active=True)
            asignados_ids = AsignacionVehiculo.objects.filter(vehicle=vehiculo).values_list('worker_id', flat=True)
            no_asignados = empleados_activos.exclude(rut__in=asignados_ids)
            self.fields['worker'].queryset = no_asignados
        else:
            # Por defecto no mostrar empleados si no hay vehículo
            self.fields['worker'].queryset = Empleado.objects.none()