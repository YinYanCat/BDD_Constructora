from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.http import require_POST
from django.contrib import messages

from .forms.PermisoForm import PermisoForm
from .factories.PermisoFactory import PermisoFactory
from .forms.HorarioForm import HorarioForm
from .factories.HorarioFactory import HorarioFactory
from .factories.ProyectoFactory import ProyectoFactory

from .forms.EmpleadoForm import EmpleadoForm
from .factories.EmpleadoFactory import EmpleadoFactory
from .factories.VehiculoFactory import VehiculoFactory
from .forms.VehiculoForm import VehiculoForm
from .forms.ProyectoForm import ProyectoForm
from .forms.EmpleadoProyectoForm import EmpleadoProyectoForm
from .factories.EmpleadoProyectoFactory import EmpleadoProyectoFactory
from .models import Proyecto, EmpleadoProyecto, Implemento, Empleado, AsignacionVehiculo, Horario, Vehiculo, AsignacionVehiculo


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
                return redirect('registro_permiso')
            except Exception as e:
                form.add_error(None, str(e))
    else:
        form = PermisoForm()
    return render(request, 'app/registro_permiso.html', {'form': form}) #LLAMAR AL HTML CORRESPONDIENTE

def lista_proyecto(request, activos = 'true'):
    if activos == 'true':
        proyectos = Proyecto.objects.filter(is_active = True)
        filter = 'Solo activos'
    elif activos == 'false':
        proyectos = Proyecto.objects.all()
        filter = 'Todos'
    else:
        proyectos = []
        filter = ''
    return render(request, 'app/lista_proyecto.html', {'proyectos': proyectos,
                                                       'filter' : filter})

def toggle_proyecto(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id = proyecto_id)
    proyecto.is_active = not proyecto.is_active
    proyecto.save()
    return redirect('lista_proyecto')

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
                return redirect('registro_horario')
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
        empleados = Empleado.objects.filter(is_active=True)
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
        empleados = Empleado.objects.filter(horario__day_of_week=day_of_week, is_active = True).distinct()

    return render(request, 'app/lista_empleados_dia.html', {
        'data': empleados,
        'day': day_of_week,
        'days': DAYS_OF_WEEK,
    })

def registrar_vehiculo(request):
    if request.method == 'POST':
        form = VehiculoForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            factory = VehiculoFactory()
            try: 
                factory.crear_vehiculo(
                    data['patente'], data['modelo'], data['año'], data['tipo'], data['estado']
                )
                messages.success(request, 'Vehiculo registrado con exito.')
                return redirect('registro_vehiculo')
            except Exception as e:
                form.add_error(None, str(e))
    else:
        form = VehiculoForm()
    return render(request, 'app/registro_vehiculo.html', {'form': form})


def lista_vehiculo(request):
    vehiculos = Vehiculo.objects.all()
    empleados_activos = Empleado.objects.filter(is_active=True)

    asignaciones = []

    for vehiculo in vehiculos:
        asignados_ids = AsignacionVehiculo.objects.filter(
            vehicle=vehiculo
        ).values_list('worker', flat=True)

        asignados = empleados_activos.filter(rut__in=asignados_ids)
        no_asignados = empleados_activos.exclude(rut__in=asignados_ids)

        asignaciones.append({
            'vehiculo': vehiculo,
            'asignados': asignados,
            'no_asignados': no_asignados
        })

    return render(request, 'app/lista_vehiculos.html', {
        'asignaciones': asignaciones
    })

def asignar_empleado(request, vehiculo_id):
    vehiculo = get_object_or_404(Vehiculo, patent=vehiculo_id)
    empleado_id = request.POST.get('empleado_id')

    if empleado_id:
        empleado = get_object_or_404(Empleado, rut=empleado_id)
        AsignacionVehiculo.objects.get_or_create(vehicle=vehiculo, worker=empleado)
        messages.success(request, f'{empleado.first_name} asignado a {vehiculo.patent}.')
    return redirect('lista_vehiculo')

@require_POST
def quitar_empleado(request, vehiculo_id, empleado_id):
    asignacion = AsignacionVehiculo.objects.filter(vehicle_id=vehiculo_id, worker_id=empleado_id)
    if asignacion.exists():
        asignacion.delete()
        messages.success(request, 'Empleado quitado correctamente.')
    return redirect('lista_vehiculo')

def toggle_empleado_status(request, empleado_rut):
    
    empleado = get_object_or_404(Empleado, rut=empleado_rut)
    
    if request.method == 'POST':
        if empleado.is_active:
            # Desactivar: eliminar asignaciones de vehículos e implementos
            AsignacionVehiculo.objects.filter(worker=empleado).delete()
            Implemento.objects.filter(worker=empleado).delete()
            empleado.is_active = False
            messages.success(request, 'Agente desactivado exitosamente')
        else:
            # Activar empleado
            empleado.is_active = True
            messages.success(request, f'Empleado {empleado.first_name} {empleado.last_name} activado correctamente.')
        
        empleado.save()
        return redirect('lista_empleados')
    
    return render(request, 'app/confirmar_toggle_empleado.html', {'empleado': empleado})

def registro_proyecto(request):
    if request.method == 'POST':
        form = ProyectoForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            factory = ProyectoFactory()
            try: 
                factory.crear_proyecto(
                    data['name'], data['start_date'], data['end_date'], data['budget'], data['description']
                )
                messages.success(request, 'Proyecto registrado con exito.')
                return redirect('registro_proyecto')
            except Exception as e:
                form.add_error(None, str(e))
    else:
        form = ProyectoForm()
    return render(request, 'app/registro_proyecto.html', {'form': form})