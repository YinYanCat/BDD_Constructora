from django import forms
from app.models import Proyecto

class ProyectoForm(forms.Form):
    name = forms.CharField(required=True, label='Nombre', max_length=200)
    start_date = forms.DateField(required=True, label='Fecha de Inicio', widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(required=True, label='Fecha de Fin', widget=forms.DateInput(attrs={'type': 'date'}))
    budget = forms.FloatField(required=True, label='Presupuesto') #  50 esta de ejemplo, puede ser modificado
    description = forms.CharField(required=True, max_length=200,
                                    label="Descripción del Proyecto",
                                    widget=forms.Textarea(attrs={
                                    'rows': 4,
                                    'cols': 40,
                                    'placeholder': 'Escribe aquí...',
                                    'style': 'resize: vertical;',
                                    'maxlength': '200'
                                    })
                                )