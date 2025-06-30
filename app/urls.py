from django.urls import path
from app.views import *
urlpatterns = [
    path('', home, name='home'),
    path('salir/', salir, name='salir'),
    path('registro_horario/', registro_horario, name='registro horario'),
]