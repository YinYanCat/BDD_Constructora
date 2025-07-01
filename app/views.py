from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages

from .forms.PermisoForm import PermisoForm
from .factories.PermisoFactory import PermisoFactory

@login_required
def home(request):
    return render(request, "app/home.html")

def salir(request):
    logout(request)
    return redirect('/')

@login_required
def registro_horario(request):
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


