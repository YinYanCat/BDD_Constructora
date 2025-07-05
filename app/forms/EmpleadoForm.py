from django import forms
from ..models import Empleado, AFP


class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['rut', 'first_name', 'last_name', 'salary', 'contract_date', 
                 'phone', 'email', 'is_active', 'afp']
        
        widgets = {
            'rut': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 12.345.678-9',
                'maxlength': '16'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del empleado'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apellido del empleado'
            }),
            'salary': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Salario en CLP',
                'step': '0.01',
                'min': '0'
            }),
            'contract_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+569 12345678'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@ejemplo.com'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'afp': forms.Select(attrs={
                'class': 'form-select'
            })
        }
        
        labels = {
            'rut': 'RUT del Empleado',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'salary': 'Salario (CLP)',
            'contract_date': 'Fecha de Contratación',
            'phone': 'Teléfono',
            'email': 'Correo Electrónico',
            'is_active': 'Empleado Activo',
            'afp': 'AFP'
        }
    
    def clean_rut(self):
        rut = self.cleaned_data.get('rut')
        if rut:
            # Eliminar espacios y puntos
            rut = rut.replace(' ', '').replace('.', '').replace('-', '')
            
            # Validar formato
            if not rut or len(rut) < 8:
                raise forms.ValidationError('RUT debe tener al menos 8 caracteres')

            # Añadir guion antes del último dígito
            if len(rut) >= 2:
                rut = rut[:-1] + '-' + rut[-1:]
            
        return rut
    
    def clean_salary(self):
        salary = self.cleaned_data.get('salary')
        if salary is not None and salary <= 0:
            raise forms.ValidationError('El salario debe ser mayor a 0')
        return salary
