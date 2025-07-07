from django import forms
from ..models import PagoEmpleado, Pago, Empleado, AFP

class PagoEmpleadoForm(forms.ModelForm):
    class Meta:
        model = PagoEmpleado
        fields = ['pago', 'empleado', 'afp']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mostrar solo pagos base sin pagoempleado asignado
        pagos_disponibles = Pago.objects.exclude(pagoempleado__isnull=False).order_by('-fecha')
        self.fields['pago'].queryset = pagos_disponibles
        self.fields['empleado'].queryset = Empleado.objects.all()
        self.fields['afp'].queryset = AFP.objects.all()