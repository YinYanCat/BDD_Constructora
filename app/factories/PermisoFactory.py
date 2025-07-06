
from..models import Permiso

class PermisoFactory:
    def crear_permiso(self, empleado, day_inicio, day_fin, tipo_permiso):
        permiso = Permiso(
            worker = empleado,
            start = day_inicio,
            end = day_fin,
            ptype = tipo_permiso
        )
        permiso.save()
        return permiso