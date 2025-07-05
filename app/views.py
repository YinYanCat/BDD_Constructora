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
from .forms.EmpleadoProyectoForm import EmpleadoProyectoForm
from .factories.EmpleadoProyectoFactory import EmpleadoProyectoFactory
from .models import Proyecto, EmpleadoProyecto, Implemento, Empleado, Horario


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
                return redirect('registro horario')
            except Exception as e:
                form.add_error(None, str(e))
    else:
        form = HorarioForm()
    return render(request, 'app/registro_horario.html', {'form': form})

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

def asignar_empleado_proyecto(request):
    if request.method == 'POST':
        form = EmpleadoProyectoForm(request.POST)
        if form.is_valid():
            try:
                factory = EmpleadoProyectoFactory()
                asignacion = factory.asignar_empleado_proyecto(
                    worker=form.cleaned_data['worker'],
                    proyect=form.cleaned_data['proyect'],
                    position=form.cleaned_data['position'],
                    bonus_pay=form.cleaned_data['bonus_pay']
                )
                messages.success(
                    request,
                    f'Empleado {asignacion.worker.first_name} {asignacion.worker.last_name} '
                    f'asignado exitosamente al proyecto {asignacion.proyect.name} '
                    f'como {asignacion.position}'
                )
                return redirect('asignar_empleado_proyecto')
            except Exception as e:
                messages.error(request, f'Error al asignar empleado: {str(e)}')
        else:
            messages.error(request, 'Por favor corrija los errores del formulario.')
    else:
        form = EmpleadoProyectoForm()
    
    return render(request, 'app/asignar_empleado_proyecto.html', {'form': form})

def lista_asignaciones(request):
    asignaciones = EmpleadoProyecto.objects.select_related('worker', 'proyect').all()
    return render(request, 'app/lista_asignaciones.html', {'asignaciones': asignaciones})
  
def lista_horario(request, rut=None):
    if rut is not None:
        horarios = Horario.objects.filter(worker = rut)
        return render(request, 'app/lista_horario_empleado.html', {'data' : horarios})
    else:
        empleados = Empleado.objects.all()
        return render(request, 'app/lista_horario.html', {'data':empleados})
    
def lista_empleados_dia(request, day_of_week=None):
    DAYS_OF_WEEK = [
        ('MON', 'Lunes'),
        ('TUES', 'Martes'),
        ('WED', 'Miércoles'),
        ('THU', 'Jueves'),
        ('FRI', 'Viernes'),
        ('SAT', 'Sábado'),
        ('SUN', 'Domingo'),
    ]
    empleados = []
    if day_of_week is not None:
        empleados = Empleado.objects.filter(horario__day_of_week=day_of_week).distinct()

    return render(request, 'app/lista_empleados_dia.html', {
        'data': empleados,
        'day': day_of_week,
        'days': DAYS_OF_WEEK,
    })

