from django import forms
from app.models import Profesion

class ProfesionForm(forms.Form):
    name = forms.CharField(required=True, label='Nombre de la Profesión', max_length=200)
    