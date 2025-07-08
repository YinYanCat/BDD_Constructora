from..models import Profesion

class ProfesionFactory:
    def crear_profesion(self, nombre):
        profesion = Profesion(
            name=nombre
        )
        profesion.save()
        return profesion