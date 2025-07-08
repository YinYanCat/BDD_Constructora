from django import forms
from ..models import PagoImplemento, PagoInsumoServicio, Implemento, Pago

class PagoImplementoForm(forms.ModelForm):
    class Meta:
        model = PagoImplemento
        fields = ['pago', 'implemento']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Obtener IDs de pagos ya asignados a PagoImplemento para evitar duplicados
        pagos_asignados = PagoImplemento.objects.values_list('pago_id', flat=True)
        
        # Filtrar para que solo muestre pagos que no estén asignados aún
        pagos_disponibles = Pago.objects.exclude(id__in=pagos_asignados).order_by('-fecha')

        self.fields['pago'].queryset = pagos_disponibles
        self.fields['implemento'].queryset = Implemento.objects.all()