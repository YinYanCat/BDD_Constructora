from..models import Horario
from django.db import IntegrityError

class HorarioFactory:
    def crear_horario(self, empleado, dia, h_inicio, h_fin):
        try:
            horario = Horario(
                worker = empleado,
                day_of_week = dia,
                start = h_inicio,
                end = h_fin
            )
        except IntegrityError:
            raise ValueError("Este empleado ya tiene un horario registrado para ese día.")
        return horario