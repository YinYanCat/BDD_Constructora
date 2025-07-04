from django.urls import path
from app.views import *
urlpatterns = [
    path('', home, name='home'),
    path('salir/', salir, name='salir'),

    path('registro_permiso/', registro_permiso, name='registro permiso'),
    path('proyecto/<int:proyecto_id>/empleados/', proyecto_empleados, name='proyecto_empleados'),
    path('implementos/', lista_implementos, name='lista_implementos'),
    path('registro_horario/', registro_horario, name='registro horario'),
    path('registro_empleado/', registro_empleado, name='registro_empleado'),
    path('lista_empleados/', lista_empleados, name='lista_empleados'),
    path('asignar_empleado_proyecto/', asignar_empleado_proyecto, name='asignar_empleado_proyecto'),
    path('lista_asignaciones/', lista_asignaciones, name='lista_asignaciones'),
]