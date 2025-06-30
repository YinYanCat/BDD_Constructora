from..models import Horario

class HorarioFactory:
    def crear_horario(self, empleado, dia, h_inicio, h_fin):
        
        horario = Horario(
            worker = empleado,
            day_of_week = dia,
            start = h_inicio,
            end = h_fin
        )
        return horario