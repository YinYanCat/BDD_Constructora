from django import forms
from ..models import PagoVehiculo, Pago, Vehiculo

class PagoVehiculoForm(forms.ModelForm):
    class Meta:
        model = PagoVehiculo
        fields = ['pago', 'vehiculo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mostrar solo pagos base sin pagovehiculo asignado
        pagos_disponibles = Pago.objects.exclude(pagovehiculo__isnull=False).order_by('-fecha')
        self.fields['pago'].queryset = pagos_disponibles
        self.fields['vehiculo'].queryset = Vehiculo.objects.all()