from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages

from .forms.PermisoForm import PermisoForm
from .factories.PermisoFactory import PermisoFactory
from .forms.HorarioForm import HorarioForm
from .factories.HorarioFactory import HorarioFactory
from .forms.EmpleadoForm import EmpleadoForm
from .factories.EmpleadoFactory import EmpleadoFactory
from .models import Proyecto, EmpleadoProyecto, Implemento, Empleado


@login_required
def home(request):
    return render(request, "app/home.html")

def salir(request):
    logout(request)
    return redirect('/')

@login_required
def registro_permiso(request):
    if request.method == 'POST':
        form = PermisoForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            factory = PermisoFactory()
            try: 
                factory.crear_permiso(
                    data['worker'], data['start'], data['end'], data['ptype']
                )
                messages.success(request, 'Permiso creado con exito.')
                form = PermisoForm()
                return redirect('registro permiso')
            except Exception as e:
                form.add_error(None, str(e))
    else:
        form = PermisoForm()
    return render(request, 'PAGINA REGISTRO PERMISO', {'form': form}) #LLAMAR AL HTML CORRESPONDIENTE

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

def registro_horario(request):
    if request.method == 'POST':
        form = HorarioForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            factory = HorarioFactory()
            try: 
                factory.crear_horario(
                    data['worker'], data['day_of_week'], data['start'], data['end']
                )
                messages.success(request, 'Horario creado con exito.')
                form = HorarioForm()
                return redirect('registro horario')
            except Exception as e:
                form.add_error(None, str(e))
    else:
        form = HorarioForm()
    return render(request, 'PAGINA REGISTRO HORARIO', {'form': form})

# @login_required  # Comentado para pruebas
def registro_empleado(request):
    if request.method == 'POST':
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            try:
                empleado = EmpleadoFactory.crear_empleado(form.cleaned_data)
                messages.success(
                    request, 
                    f'Empleado {empleado.first_name} {empleado.last_name} registrado exitosamente!'
                )
                return redirect('registro_empleado')
            except Exception as e:
                messages.error(request, f'Error al registrar empleado: {str(e)}')
        else:
            messages.error(request, 'Por favor corrija los errores del formulario.')
    else:
        form = EmpleadoForm()
    
    return render(request, 'app/registro_empleado.html', {'form': form})

def lista_empleados(request):
    empleados = Empleado.objects.select_related('afp').all()
    return render(request, 'app/lista_empleados.html', {'empleados': empleados})