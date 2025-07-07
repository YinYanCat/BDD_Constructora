from django import forms
from ..models import Factura

class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = ['empleado', 'capacitacion', 'monto', 'detalle', 'estado']
        widgets = {
            'detalle': forms.Textarea(attrs={'rows': 3}),
        }
