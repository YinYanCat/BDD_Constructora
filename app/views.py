from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages

from .forms.HorarioForm import HorarioForm
from .factories.HorarioFactory import HorarioFactory

@login_required
def home(request):
    return render(request, "app/home.html")

def salir(request):
    logout(request)
    return redirect('/')

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
                form = HorarioForm()
                return redirect('registro horario')
            except Exception as e:
                form.add_error(None, str(e))
    else:
        form = HorarioForm()
    return render(request, 'PAGINA REGISTRO HORARIO', {'form': form})

