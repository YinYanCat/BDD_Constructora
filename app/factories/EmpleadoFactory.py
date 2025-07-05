from django.db import transaction
from ..models import Empleado, AFP
from django.core.exceptions import ValidationError


class EmpleadoFactory:
    
    @staticmethod
    @transaction.atomic
    def crear_empleado(form_data):
        try:
            # Validar que el RUT no exista
            if Empleado.objects.filter(rut=form_data['rut']).exists():
                raise ValidationError(f"Ya existe un empleado con RUT {form_data['rut']}")
            
            # Validar que la AFP exista
            afp = form_data['afp']
            if not isinstance(afp, AFP):
                raise ValidationError("AFP inválida")
            
            # Crear el empleado
            empleado = Empleado.objects.create(
                rut=form_data['rut'],
                first_name=form_data['first_name'],
                last_name=form_data['last_name'],
                salary=form_data['salary'],
                contract_date=form_data['contract_date'],
                phone=form_data['phone'],
                email=form_data['email'],
                is_active=form_data['is_active'],
                afp=afp
            )
            
            return empleado
            
        except ValidationError:
            raise
        except Exception as e:
            raise ValidationError(f"Error al crear empleado: {str(e)}")
    
    @staticmethod
    def validar_rut_disponible(rut):
        return not Empleado.objects.filter(rut=rut).exists()
    
    @staticmethod
    def obtener_afps_disponibles():
        return AFP.objects.all()
