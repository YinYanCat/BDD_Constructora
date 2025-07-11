from ..models import AsignacionVehiculo

class EmpleadoVehiculoFactory:
    def crear_asignacion(self,vehicle, worker):
        asignacion = AsignacionVehiculo(
            vehicle = vehicle,
            worker = worker
        )
        asignacion.save()
        return asignacion