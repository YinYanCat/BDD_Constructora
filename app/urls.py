from django.urls import path
from app.views import *
urlpatterns = [
    path('', home, name='home'),
    path('salir/', salir, name='salir'),
    path('registro_permiso/', registro_horario, name='registro permiso'),
    path('proyecto/<int:proyecto_id>/empleados/', proyecto_empleados, name='proyecto_empleados'),
    path('implementos/', lista_implementos, name='lista_implementos'),
]