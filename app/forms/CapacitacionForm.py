from django import forms
from ..models import Capacitacion

class CapacitacionForm(forms.ModelForm):
    class Meta:
        model = Capacitacion
        fields = ['name', 'institution', 'end_date', 'cert']
        widgets = {
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }