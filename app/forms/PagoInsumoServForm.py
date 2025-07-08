from django import forms
from ..models import PagoInsumoServicio, Pago, Capacitacion

class PagoInsumoServForm(forms.ModelForm):
    class Meta:
        model = PagoInsumoServicio
        fields = ['pago', 'capacitacion']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mostrar solo pagos base sin pagoinsumo asignado
        pagos_disponibles = Pago.objects.exclude(pagoinsumo__isnull=False).order_by('-fecha')
        self.fields['pago'].queryset = pagos_disponibles
        self.fields['capacitacion'].queryset = Capacitacion.objects.all()
