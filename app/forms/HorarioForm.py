from django import forms
from app.models import Empleado

class HorarioForm(forms.Form):
    DAYS_OF_WEEK = [
        ('MON', 'Monday'),
        ('TUES', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
        ('SAT', 'Saturday'),
        ('SUN', 'Sunday')
    ]
    worker = forms.ModelChoiceField(queryset=Empleado.objects.all(), required=True, label='Empleado')
    day_of_week = forms.ChoiceField(required=True,  choices=DAYS_OF_WEEK, label='Dia de la semana')
    start = forms.TimeField(required=True, label='Hora de inicio')
    end = forms.TimeField(required=True, label='Hora de fin')