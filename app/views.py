from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db.models import Q
from django.db import transaction

from .factories.ImplementoFactory import ImplementoFactory
from .forms.ImplementoForm import ImplementoForm
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

from .forms.CapacitacionForm import CapacitacionForm
from .forms.FacturaForm import FacturaForm
from .forms.PagoForm import PagoForm
from .forms.PagoEmpleadoForm import PagoEmpleadoForm
from .forms.PagoInsumoServForm import PagoInsumoServForm
from .forms.PagoVehiculoForm import PagoVehiculoForm
from .forms.PagoImplementoForm import PagoImplementoForm

from .models import Proyecto, EmpleadoProyecto, Implemento, Empleado, AsignacionVehiculo, Horario, Vehiculo, AsignacionVehiculo, Capacitacion, Factura, Pago, PagoEmpleado, PagoInsumoServicio, PagoImplemento, PagoVehiculo

from .factories.ProfesionFactory import ProfesionFactory
from .forms.ProfesionForm import ProfesionForm
from .factories.AFPFactory import AFPFactory
from .forms.AFPForm import AFPForm

@login_required
def home(request):
    return render(request, "app/home.html")

@login_required
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
    return render(request, 'app/registro_permiso.html', {'form': form}) 

@login_required
def lista_permisos(request):
    return render(request, 'app/lista_permisos.html')

@login_required
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
@login_required
def toggle_proyecto(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id = proyecto_id)
    proyecto.is_active = not proyecto.is_active
    proyecto.save()
    return redirect('lista_proyecto')

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

@login_required
def registro_implemento(request):
    if request.method == 'POST':
        form = ImplementoForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            factory = ImplementoFactory()
            try:
                factory.crear_implemento(
                    data['itype'], data['worker'], data['description']
                )
                messages.success(request, 'Implemento registrado con exito.')
                return redirect('registro_implemento')
            except Exception as e:
                form.add_error(None, str(e))
    else:
        form = ImplementoForm()
    return render(request, 'app/registro_implemento.html', {'form': form,})

@login_required
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

@login_required
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

@login_required
def lista_empleados(request, activos = 'true'):
    if activos == 'true':
        empleados = Empleado.objects.filter(is_active=True)
        filter = 'Solo activos'
    elif activos == 'false':
        empleados = Empleado.objects.all()
        filter = 'Todos'
    else:
        empleados = []
        filter = ''
    return render(request, 'app/lista_empleados.html', {'empleados': empleados, 'filter': filter})

@login_required
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

@login_required
def lista_asignaciones(request):
    asignaciones = EmpleadoProyecto.objects.select_related('worker', 'proyect').all()
    return render(request, 'app/lista_asignaciones.html', {'asignaciones': asignaciones})

@login_required
def lista_horario(request, rut=None):
    if rut is not None:
        horarios = Horario.objects.filter(worker = rut)
        return render(request, 'app/lista_horario_empleado.html', {'data' : horarios})
    else:
        empleados = Empleado.objects.filter(is_active=True)
        return render(request, 'app/lista_horario.html', {'data':empleados})

@login_required
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

@login_required
def registrar_vehiculo(request):
    if request.method == 'POST':
        form = VehiculoForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            factory = VehiculoFactory()
            try: 
                factory.crear_vehiculo(
                    data['patent'], data['model'], data['year'], data['vtype'], data['status']
                )
                messages.success(request, 'Vehiculo registrado con exito.')
                return redirect('registrar_vehiculo')
            except Exception as e:
                form.add_error(None, str(e))
    else:
        form = VehiculoForm()
    return render(request, 'app/registro_vehiculo.html', {'form': form})

@login_required
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
            'asdignados': asignados,
            'no_asignaos': no_asignados
        })

    return render(request, 'app/lista_vehiculos.html', {
        'vehiculos': vehiculos
    })

@login_required
def asignar_empleado(request, vehiculo_id):
    vehiculo = get_object_or_404(Vehiculo, patent=vehiculo_id)
    empleado_id = request.POST.get('empleado_id')

    if empleado_id:
        empleado = get_object_or_404(Empleado, rut=empleado_id)
        AsignacionVehiculo.objects.get_or_create(vehicle=vehiculo, worker=empleado)
        messages.success(request, f'{empleado.first_name} asignado a {vehiculo.patent}.')
    return redirect('lista_vehiculo')

@login_required
def quitar_empleado(request, vehiculo_id, empleado_id):
    if request.method == 'POST':
        asignacion = AsignacionVehiculo.objects.filter(vehicle_id=vehiculo_id, worker_id=empleado_id)
        if asignacion.exists():
            asignacion.delete()
            messages.success(request, 'Empleado quitado correctamente.')
        return redirect('lista_vehiculo')
    else :
        return redirect('home')

@login_required
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

@login_required
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

@login_required
def registro_capacitacion(request):
    if request.method == 'POST':
        form = CapacitacionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registro_capacitacion')  # redirige a sí misma para que se actualice
    else:
        form = CapacitacionForm()

    return render(request, 'app/registro_capacitacion.html', {'form': form,})

@login_required
def lista_capacitacion(request):
    capacitaciones = Capacitacion.objects.all().order_by('-end_date')
    return render(request, 'app/lista_capacitacion.html', { 'capacitaciones': capacitaciones })

@login_required
def registro_factura(request):
    if request.method == 'POST':
        form = FacturaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registro_factura')  # redirige a sí misma
    else:
        form = FacturaForm()
    return render(request, 'app/registro_factura.html', {'form': form,})

@login_required
def lista_factura(request):
    facturas = Factura.objects.select_related('empleado', 'capacitacion').all().order_by('-id')
    return render(request, 'app/lista_factura.html', {'facturas': facturas})

@login_required
def pagos_view(request):
    query = request.GET.get('q', '')
    tipo = request.GET.get('tipo', '')

    pagos_base = Pago.objects.filter(
        Q(descripcion__icontains=query) |
        Q(monto__icontains=query) |
        Q(fecha__icontains=query)
    ).order_by('-fecha')

    pagos_empleado = PagoEmpleado.objects.select_related('pago', 'empleado', 'afp').all() if tipo in ['', 'empleado'] else []
    pagos_insumo = PagoInsumoServicio.objects.select_related('pago', 'capacitacion').all() if tipo in ['', 'insumo'] else []
    pagos_vehiculo = PagoVehiculo.objects.select_related('pago', 'vehiculo').all() if tipo in ['', 'vehiculo'] else []
    pagos_implemento = PagoImplemento.objects.select_related('pago', 'implemento').all() if tipo in ['', 'implemento'] else []

    mensaje = ''
    pago_form = PagoForm()
    tipo_pago_form = None
    tipo_form_activo = ''  # Guarda el tipo de formulario activo

    if request.method == 'POST':
        if 'crear_pago' in request.POST:
            pago_form = PagoForm(request.POST)
            if pago_form.is_valid():
                nuevo_pago = pago_form.save()
                mensaje = f'Pago #{nuevo_pago.id} creado. Ahora asigna su tipo abajo.'
                pago_form = PagoForm()  # Limpiar form después de guardar

        elif 'tipo_form' in request.POST:
            tipo_form_activo = request.POST.get('tipo_form', '')
            if tipo_form_activo == 'empleado':
                tipo_pago_form = PagoEmpleadoForm(request.POST)
            elif tipo_form_activo == 'insumo':
                tipo_pago_form = PagoInsumoServForm(request.POST)
            elif tipo_form_activo == 'vehiculo':
                tipo_pago_form = PagoVehiculoForm(request.POST)
            elif tipo_form_activo == 'implemento':
                tipo_pago_form = PagoImplementoForm(request.POST)
            else:
                tipo_pago_form = None

            if tipo_pago_form and tipo_pago_form.is_valid():
                tipo_pago_form.save()
                mensaje = "Tipo de pago asignado correctamente."
                tipo_pago_form = None
                tipo_form_activo = ''

    context = {
        'query': query,
        'tipo': tipo,
        'pagos_base': pagos_base,
        'pagos_empleado': pagos_empleado,
        'pagos_insumo': pagos_insumo,
        'pagos_vehiculo': pagos_vehiculo,
        'pagos_implemento': pagos_implemento,
        'pago_form': pago_form,
        'tipo_pago_form': tipo_pago_form,
        'mensaje': mensaje,
        'tipo_form_activo': tipo_form_activo,
    }

    return render(request, 'app/pagos.html', context)

@login_required
def crear_profesion(request):
    if request.method == 'POST':
        form = ProfesionForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            factory = ProfesionFactory()
            try: 
                factory.crear_profesion(data['name'])
                messages.success(request, 'Profesión creada con éxito.')
                return redirect('crear_profesion')
            except Exception as e:
                form.add_error(None, str(e))
    else:
        form = ProfesionForm()
    return render(request, 'app/crear_profesion.html', {'form': form})

@login_required
def crear_afp(request):
    if request.method == 'POST':
        form = AFPForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            factory = AFPFactory()
            try: 
                factory.crear_afp(data['rut'], data['name'])
                messages.success(request, 'AFP creada con éxito.')
                return redirect('crear_afp')
            except Exception as e:
                form.add_error(None, str(e))
    else:
        form = AFPForm()
    return render(request, 'app/crear_afp.html', {'form': form})
