from app.models import AFP

from app.models import AFP

class AFPFactory:
    def crear_afp(self, rut, nombre):
        afp = AFP(rut=rut, name=nombre)
        afp.save()
        return afp