from django.db import transaction
from ..models import EmpleadoProyecto, Empleado, Proyecto
from django.core.exceptions import ValidationError


class EmpleadoProyectoFactory:

    @transaction.atomic
    def asignar_empleado_proyecto(self, worker, proyect, position, bonus_pay=0):
        # Validaciones
        if not worker:
            raise ValidationError("Debe seleccionar un empleado")
        
        if not proyect:
            raise ValidationError("Debe seleccionar un proyecto")
            
        if not position or not position.strip():
            raise ValidationError("El rol/posición es obligatorio")
        
        if bonus_pay < 0:
            raise ValidationError("La bonificación no puede ser negativa")
        
        # Verificar que el empleado esté activo
        if not worker.is_active:
            raise ValidationError(f"El empleado {worker.first_name} {worker.last_name} no está activo")
        
        # Verificar que el proyecto esté activo
        if not proyect.is_active:
            raise ValidationError(f"El proyecto {proyect.name} no está activo")
        
        # Verificar que el empleado no esté ya asignado a este proyecto
        if EmpleadoProyecto.objects.filter(worker=worker, proyect=proyect).exists():
            raise ValidationError(
                f"El empleado {worker.first_name} {worker.last_name} ya está asignado al proyecto {proyect.name}"
            )
        
        # Crear la asignación
        asignacion = EmpleadoProyecto.objects.create(
            worker=worker,
            proyect=proyect,
            position=position.strip(),
            bonus_pay=bonus_pay
        )
        
        return asignacion
    
    def obtener_empleados_disponibles(self):
        return Empleado.objects.filter(is_active=True)
    
    def obtener_proyectos_disponibles(self):
        return Proyecto.objects.filter(is_active=True)
    
    def obtener_asignaciones_empleado(self, empleado):
        return EmpleadoProyecto.objects.filter(worker=empleado).select_related('proyect')
    
    def obtener_empleados_proyecto(self, proyecto):
        return EmpleadoProyecto.objects.filter(proyect=proyecto).select_related('worker')
