from django import forms
from app.models import Empleado, Horario
from django.core.exceptions import ValidationError

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

    def clean(self):
        cleaned_data = super().clean()
        worker = cleaned_data.get('worker')
        day_of_week = cleaned_data.get('day_of_week')
        start = cleaned_data.get('start')
        end = cleaned_data.get('end')

        # Validar que la hora de inicio sea menor a la hora de fin
        if start and end and start >= end:
            raise ValidationError("La hora de inicio debe ser menor que la hora de fin.")

        # Validar que no exista ya un horario con ese empleado y día
        if worker and day_of_week:
            if Horario.objects.filter(worker=worker, day_of_week=day_of_week).exists():
                raise ValidationError("Ese empleado ya tiene un horario asignado para ese día.")

        return cleaned_data