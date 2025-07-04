from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    #Django proporciona un abstracto de usuario
    #contiene
    #first_name
    #last_name
    #password
    #email
    #is_active
    #is_superuser
    #is_staff
    pass

class Cambio(models.Model):
    user = models.ForeignKey(Usuario, on_delete=models.PROTECT)
    date = models.DateTimeField(null=False)
    id_reg = models.IntegerField(null=False)
    table_name = models.CharField(null=False, max_length=200)
    prev_values = models.TextField(null=False)
    new_values = models.TextField(null=False)

class AFP(models.Model):
    rut = models.CharField(primary_key=True, max_length=16)
    name = models.CharField(null=False, max_length=200)

class Empleado(models.Model):
    rut = models.CharField(primary_key=True, max_length=16)
    first_name = models.CharField(null=False, max_length=200)
    last_name = models.CharField(null=False, max_length=200)
    salary = models.FloatField(null=False)    
    contract_date = models.DateField()
    phone = models.CharField(null=False, max_length=16)
    email = models.CharField(null=False, max_length=200)
    is_active = models.BooleanField(null=False)
    afp = models.ForeignKey(AFP, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.rut} - {self.first_name} {self.last_name}'

class Horario(models.Model):
    DAYS_OF_WEEK = [
        ('MON', 'Monday'),
        ('TUES', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
        ('SAT', 'Saturday'),
        ('SUN', 'Sunday')
    ]
    worker = models.ForeignKey(Empleado, null=False, on_delete=models.CASCADE)
    day_of_week = models.CharField(null=False, max_length=4, choices=DAYS_OF_WEEK)
    start = models.TimeField(null=False)
    end = models.TimeField(null=False)

    class Meta:
        unique_together = ('worker', 'day_of_week')

class Proyecto(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(null=False, max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    budget = models.FloatField()
    description = models.CharField(null=False, max_length=200)
    is_active = models.BooleanField(default=True)  # ← esto te permite marcarlo como activo/inactivo

class EmpleadoProyecto(models.Model):
    worker = models.ForeignKey(Empleado, null=False, on_delete=models.PROTECT)
    proyect = models.ForeignKey(Proyecto, null=False, on_delete=models.PROTECT)
    bonus_pay = models.FloatField(default=0)
    position = models.CharField(null=False, max_length=200)

class Capacitacion(models.Model):
    name = models.CharField(max_length=100)
    institution = models.CharField(max_length=100)
    end_date = models.DateField()
    cert = models.CharField(max_length=100)

class EmpleadoCapacitacion(models.Model):
    worker = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    id_capacitacion = models.ForeignKey(Capacitacion, on_delete=models.CASCADE)
    aproved = models.BooleanField(default=False)

class FacturaEmpleado(models.Model):
    worker = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    total = models.FloatField()
    detail = models.TextField()

class FacturaCapacitacion(models.Model):
    id_capacitacion = models.ForeignKey(Capacitacion, on_delete=models.CASCADE)
    total = models.FloatField()
    detail = models.TextField()

class Vehiculo(models.Model):
    patent = models.CharField(primary_key=True, max_length=10)
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    status = models.CharField(max_length=50)
    vtype = models.CharField(max_length=50)

class AsignacionVehiculo(models.Model):
    vehicle = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    worker = models.ForeignKey(Empleado, on_delete=models.CASCADE)

class Implemento(models.Model):
    id = models.AutoField(primary_key=True)
    itype = models.CharField(max_length=100)
    description = models.TextField()
    worker = models.ForeignKey(Empleado, on_delete=models.CASCADE)

class PagoBien(models.Model):
    date = models.DateField()
    total = models.FloatField()
    description = models.TextField()

class PagoSueldo(models.Model):
    date = models.DateField()
    total = models.FloatField()
    description = models.TextField()
    worker = models.ForeignKey(Empleado, on_delete=models.CASCADE)

class PagoVehiculo(models.Model):
    vehicle = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    id_pay = models.ForeignKey(PagoBien, on_delete=models.CASCADE)

class PagoImplemento(models.Model):
    id_implement = models.ForeignKey(Implemento, on_delete=models.CASCADE)
    id_pay = models.ForeignKey(PagoBien, on_delete=models.CASCADE)

class Permiso(models.Model):
    worker = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    start = models.DateField()
    end = models.DateField()
    ptype = models.CharField(max_length=50)