from django.urls import path
from app.views import *
urlpatterns = [
    path('', home, name='home'),
    path('salir/', salir, name='salir'),

    path('registro_proyecto/', registro_proyecto, name='registro_proyecto'),
    path('lista_proyecto/', lista_proyecto, name='lista_proyecto'),
    path('lista_proyecto/<str:activos>/', lista_proyecto, name='lista_proyecto'),
    path('toggle_proyecto/<int:proyecto_id>/', toggle_proyecto, name='toggle_proyecto'),
    path('proyecto/<int:proyecto_id>/empleados/', proyecto_empleados, name='proyecto_empleados'),

    path('implementos/', lista_implementos, name='lista_implementos'),
    path('implemento/<int:implemento_id>/cambiar_empleado/', cambiar_empleado_implemento, name='cambiar_empleado_implemento'),
    path('registro_implemento/', registro_implemento, name='registro_implemento'),
  
    path('registro_empleado/', registro_empleado, name='registro_empleado'),
    path('empleado/<str:empleado_rut>/toggle/', toggle_empleado_status, name='toggle_empleado_status'),
    path('lista_empleados/', lista_empleados, name='lista_empleados'),
    path('lista_empleados/<str:activos>/', lista_empleados, name='lista_empleados'),
    path('datos_empleado/<str:rut>/', datos_empleado, name='datos_empleado'),

    path('asignar_empleado_proyecto/', asignar_empleado_proyecto, name='asignar_empleado_proyecto'),
    path('lista_asignaciones/', lista_asignaciones, name='lista_asignaciones'),
  
    path('registro_horario/', registro_horario, name='registro_horario'),
    path('registro_horario/<str:rut>/', registro_horario, name='registro_horario'),
    path('lista_empleados_dia/', lista_empleados_dia, name='lista_empleados_dia'),
    path('lista_empleados_dia/<str:day_of_week>/', lista_empleados_dia, name='lista_empleados_dia'),

    path('registrar_vehiculo/', registrar_vehiculo, name='registrar_vehiculo'),
    path('detalle_vehiculo/<str:patent>', detalle_vehiculo, name='detalle_vehiculo'),
    path('vehiculo/<str:patent>/desasignar/<str:rut>/', desasignar_empleado, name='desasignar_empleado'),
    path('vehiculos/', lista_vehiculo, name='lista_vehiculo'),

    path('lista_capacitacion/', lista_capacitacion, name='lista_capacitacion'),
    path('registro_capacitacion/', registro_capacitacion, name='registro_capacitacion'),

    path('lista_factura/', lista_factura, name='lista_factura'),
    path('registro_factura/', registro_factura, name='registro_factura'),

    path('registro_permiso/', registro_permiso, name='registro_permiso'),
    path('lista_permisos/', lista_permisos, name='lista_permisos'),

    path('pagos/', pagos_view, name='vista_pagos'),
    path('crear_profesion/', crear_profesion, name='crear_profesion'),
    path('crear_afp/', crear_afp, name='crear_afp'),
]