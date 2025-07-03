from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Proyecto, EmpleadoProyecto, Implemento

@login_required
def home(request):
    return render(request, "app/home.html")

def salir(request):
    logout(request)
    return redirect('/')

@login_required
def proyecto_empleados(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    empleados_proyecto = EmpleadoProyecto.objects.filter(proyect=proyecto)
    return render(request, 'app/proyecto_empleados.html', {
        'proyecto': proyecto,
        'empleados_proyecto': empleados_proyecto,
    })

@login_required
def lista_implementos(request):
    implementos = Implemento.objects.select_related('worker').all()
    return render(request, 'app/lista_implementos.html', {'implementos': implementos})