from django import forms
from django.utils import timezone
from django.core.exceptions import ValidationError

class VehiculoForm(forms.Form):
    patent = forms.CharField(required=True, label='Patente', max_length=10)
    model = forms.CharField(required=True, label='Año del Vehiculo', max_length=100)
    year = forms.IntegerField(required=True, label='Año del Vehiculo')
    vtype = forms.CharField(required=True, label='Tipo de Vehiculo', max_length=50)
    status = forms.CharField(required=True, label='Estado del Vehiculo', max_length=50)

    def clean(self):
            cleaned_data = super().clean()
            year = cleaned_data.get('year')
            current_year = timezone.now().year
    
            if year is not None and year > current_year:
                raise ValidationError({'year': f'El año no puede ser mayor al actual ({current_year}).'})
    
            return cleaned_data