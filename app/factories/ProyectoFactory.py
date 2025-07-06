from..models import Proyecto

class ProyectoFactory:
    def crear_proyecto(self, name, start, end, budget, description):
        
        proyecto = Proyecto(
            name = name,
            start_date = start,
            end_date = end,
            budget = budget,
            description = description
        )
        proyecto.save()
        return proyecto