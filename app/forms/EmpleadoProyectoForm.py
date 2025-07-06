from django import forms
from ..models import EmpleadoProyecto, Empleado, Proyecto
from typing import cast
from django.forms.models import ModelChoiceField


class EmpleadoProyectoForm(forms.ModelForm):
    class Meta:
        model = EmpleadoProyecto
        fields = ['worker', 'proyect', 'position', 'bonus_pay']
        
        widgets = {
            'worker': forms.Select(attrs={
                'class': 'form-control',
                'style': 'width: 100%; padding: 8px;'
            }),
            'proyect': forms.Select(attrs={
                'class': 'form-control',
                'style': 'width: 100%; padding: 8px;'
            }),
            'position': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Jefe de Obra, Supervisor, Operario...',
                'style': 'width: 100%; padding: 8px;'
            }),
            'bonus_pay': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Bonificación adicional (opcional)',
                'step': '0.01',
                'min': '0',
                'style': 'width: 100%; padding: 8px;'
            }),
        }
        
        labels = {
            'worker': 'Empleado',
            'proyect': 'Proyecto',
            'position': 'Rol/Posición en el Proyecto',
            'bonus_pay': 'Bonificación Adicional',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['worker'] = cast(ModelChoiceField, self.fields['worker'])
        self.fields['worker'].queryset = Empleado.objects.filter(is_active=True)

        self.fields['proyect'] = cast(ModelChoiceField, self.fields['proyect'])
        self.fields['proyect'].queryset = Proyecto.objects.filter(is_active=True)


    def clean(self):
        cleaned_data = super().clean()
        worker = cleaned_data.get('worker')
        proyect = cleaned_data.get('proyect')
        
        # Validar que el empleado no esté ya asignado a este proyecto
        if worker and proyect:
            if EmpleadoProyecto.objects.filter(worker=worker, proyect=proyect).exists():
                raise forms.ValidationError(
                    f'El empleado {worker.first_name} {worker.last_name} ya está asignado al proyecto {proyect.name}'
                )
        
        return cleaned_data
    
    def clean_bonus_pay(self):
        bonus_pay = self.cleaned_data.get('bonus_pay')
        if bonus_pay is not None and bonus_pay < 0:
            raise forms.ValidationError('La bonificación no puede ser negativa')
        return bonus_pay or 0
