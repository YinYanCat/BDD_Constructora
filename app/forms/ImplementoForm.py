from django import forms
from django.utils import timezone
from django.core.exceptions import ValidationError
from app.models import Empleado

class ImplementoForm(forms.Form):
    itype = forms.CharField(required=True, label='Tipo', max_length=100)
    worker = forms.ModelChoiceField(queryset=Empleado.objects.all(), required=False, label='Empleado')
    description = forms.CharField(required=True, max_length=200,
                                    label="Descripción del Implemento",
                                    widget=forms.Textarea(attrs={
                                    'rows': 4,
                                    'cols': 40,
                                    'placeholder': 'Escribe aquí...',
                                    'style': 'resize: vertical;',
                                    'maxlength': '200'
                                    })
                                )
