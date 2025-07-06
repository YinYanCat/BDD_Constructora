from..models import Vehiculo

class VehiculoFactory:
    def crear_vehiculo(self, patente, modelo, año, tipo, estado):
        
        vehiculo = Vehiculo(
            patent = patente,
            model = modelo,
            year = año,
            vtype = tipo,
            status = estado
        )
        vehiculo.save()
        return vehiculo