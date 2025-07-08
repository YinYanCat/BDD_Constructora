from django.urls import path
from app.views import *
urlpatterns = [
    path('', home, name='home'),
    path('salir/', salir, name='salir'),

    path('registro_permiso/', registro_permiso, name='registro_permiso'),

    path('registro_proyecto/', registro_proyecto, name='registro_proyecto'),
    path('lista_proyecto/', lista_proyecto, name='lista_proyecto'),
    path('lista_proyecto/<str:activos>/', lista_proyecto, name='lista_proyecto'),
    path('toggle_proyecto/<int:proyecto_id>/', toggle_proyecto, name='toggle_proyecto'),
    path('proyecto/<int:proyecto_id>/empleados/', proyecto_empleados, name='proyecto_empleados'),

    path('implementos/', lista_implementos, name='lista_implementos'),
  
    path('registro_empleado/', registro_empleado, name='registro_empleado'),
    path('empleado/<str:empleado_rut>/toggle/', toggle_empleado_status, name='toggle_empleado_status'),
    path('lista_empleados/', lista_empleados, name='lista_empleados'),
    path('asignar_empleado_proyecto/', asignar_empleado_proyecto, name='asignar_empleado_proyecto'),
    path('lista_asignaciones/', lista_asignaciones, name='lista_asignaciones'),
  
    path('registro_horario/', registro_horario, name='registro_horario'),
    path('lista_horario/', lista_horario, name='lista_horario'),
    path('lista_horario/<str:rut>/', lista_horario, name='lista_horario_empleado'),
    path('lista_empleados_dia/', lista_empleados_dia, name='lista_empleados_dia'),
    path('lista_empleados_dia/<str:day_of_week>/', lista_empleados_dia, name='lista_empleados_dia'),

    path('registrar_vehiculo/', registrar_vehiculo, name='registrar_vehiculo'),
    path('vehiculos/', lista_vehiculo, name='lista_vehiculo'),
    path('vehiculos/<str:vehiculo_id>/asignar/', asignar_empleado, name='asignar_empleado'),
    path('vehiculos/<str:vehiculo_id>/quitar/<str:empleado_id>/', quitar_empleado, name='quitar_empleado'),

    path('registrar_capacitacion/', registrar_capacitacion, name='registrar_capacitacion'),
    path('registrar_factura/', registrar_factura, name='registrar_factura'),
    path('pagos/', pagos_view, name='vista_pagos'),
  
    path('registro_permisos/', registro_permiso, name='registro_permisos'),
    path('lista_permisos/', lista_permisos, name='lista_permisos'),


    path('crear_profesion/', crear_profesion, name='crear_profesion'),
    
    path('crear_afp/', crear_afp, name='crear_afp'),
]