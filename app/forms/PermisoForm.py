
from django import forms
from app.models import Permiso, Empleado

class PermisoForm(forms.Form):
    worker = forms.ModelChoiceField(queryset=Empleado.objects.all(), required=True, label='Empleado')
    start = forms.DateField(required=True, label='Fecha de Inicio', widget=forms.DateInput(attrs={'type': 'date'}))
    end = forms.DateField(required=True, label='Fecha de Fin', widget=forms.DateInput(attrs={'type': 'date'}))
    ptype = forms.CharField(required=True, label='Tipo de Permiso', max_length=50) #  50 esta de ejemplo, puede ser modificado