# jugadores/views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import Jugador, Carpeta, PDF
from .forms import JugadorForm, CarpetaForm, PDFForm, JugadorSearchForm
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from .forms import CustomLoginForm
from django.contrib import messages


@login_required
def lista_jugadores(request):
    form = JugadorSearchForm(request.GET)  # Crear el formulario con los datos de la búsqueda
    jugadores = Jugador.objects.all()

    # Si el formulario es válido y contiene valores de búsqueda
    if form.is_valid():
        nombre = form.cleaned_data.get('nombre')
        equipo = form.cleaned_data.get('equipo')
        categoria = form.cleaned_data.get('categoria')
        ano = form.cleaned_data.get('ano')
        posicion = form.cleaned_data.get('posicion')
        trayectoria = form.cleaned_data.get('trayectoria')
        pais = form.cleaned_data.get('pais')

        # Aplicamos filtros a la queryset de jugadores
        if nombre:
            jugadores = jugadores.filter(nombre__icontains=nombre)
        if equipo:
            jugadores = jugadores.filter(equipo__icontains=equipo)
        if categoria:
            jugadores = jugadores.filter(categoria__icontains=categoria)
        if ano:
            jugadores = jugadores.filter(ano__year=ano)
        if posicion:
            jugadores = jugadores.filter(posicion__icontains=posicion)
        
        if pais:
            jugadores = jugadores.filter(pais__icontains=pais)

    context = {
        'jugadores': jugadores,
        'form': form,  # Pasamos el formulario al contexto para renderizarlo en la plantilla
    }
    return render(request, 'jugadores/lista_jugadores.html', context)


@login_required
def crear_jugador(request):
    if request.method == 'POST':
        form = JugadorForm(request.POST, request.FILES)
        perfil_pdf = request.FILES.get('perfil_pdf')  # Obtén el PDF del perfil

        if form.is_valid():
            jugador = form.save()
            if perfil_pdf:  # Si se ha subido un PDF
                # Guarda el PDF como quieras. Este es solo un ejemplo:
                pdf = PDF(archivo=perfil_pdf, jugador=jugador)
                pdf.save()
            return redirect('jugadores:lista_jugadores')
    else:
        form = JugadorForm()
        
    return render(request, 'jugadores/crear_jugador.html', {'form': form})
@login_required
def detalle_jugador(request, jugador_id):
    # Obtiene el jugador por su ID
    jugador = get_object_or_404(Jugador, id=jugador_id)
    
    # Obtener solo las carpetas raíz (sin carpeta_padre)
    carpetas_raiz = jugador.carpetas.filter(carpeta_padre__isnull=True)
    
    context = {
        'jugador': jugador,
        'carpetas': carpetas_raiz  # Solo las carpetas raíz
    }
    
    return render(request, 'jugadores/detalle_jugador.html', context)


@login_required
def crear_carpeta(request, jugador_id, carpeta_padre_id=None):
    jugador = get_object_or_404(Jugador, id=jugador_id)
    carpeta_padre = get_object_or_404(Carpeta, id=carpeta_padre_id) if carpeta_padre_id else None
    
    if request.method == 'POST':
        form = CarpetaForm(request.POST)
        if form.is_valid():
            carpeta = form.save(commit=False)
            carpeta.jugador = jugador
            carpeta.carpeta_padre = carpeta_padre  # Asignar la carpeta padre si existe
            carpeta.save()
            return redirect('jugadores:detalle_jugador', jugador_id=jugador.id)
    else:
        form = CarpetaForm()

    return render(request, 'jugadores/crear_carpeta.html', {
        'form': form,
        'jugador': jugador,
        'carpeta_padre': carpeta_padre
    })

@login_required
def crear_subcarpeta(request, carpeta_id):
    # Obtener la carpeta padre
    carpeta_padre = get_object_or_404(Carpeta, id=carpeta_id)
    
    # Obtener el jugador de la carpeta padre
    jugador = carpeta_padre.jugador  # Aquí obtenemos el jugador a partir de la carpeta padre
    
    if request.method == 'POST':
        form = CarpetaForm(request.POST)
        if form.is_valid():
            # Crear una nueva subcarpeta y asignarla al jugador y carpeta padre
            subcarpeta = form.save(commit=False)
            subcarpeta.jugador = jugador  # Asignar el jugador de la carpeta padre a la subcarpeta
            subcarpeta.carpeta_padre = carpeta_padre  # Asignar la carpeta padre
            subcarpeta.save()
            return redirect('jugadores:detalle_carpeta', carpeta_id=carpeta_padre.id)
    else:
        form = CarpetaForm()
    
    return render(request, 'jugadores/crear_carpeta.html', {
        'form': form,
        'carpeta_padre': carpeta_padre,
        'jugador': jugador  # Pasar el jugador al contexto si es necesario
    })


@login_required
def detalle_carpeta(request, carpeta_id):
    carpeta = get_object_or_404(Carpeta, id=carpeta_id)
    
    # Obtener las subcarpetas de la carpeta actual
    subcarpetas = carpeta.subcarpetas.all()
    
    # Obtener los PDFs de la carpeta actual
    pdfs = carpeta.pdfs.all()
    
    return render(request, 'jugadores/detalle_carpeta.html', {
        'carpeta': carpeta,
        'subcarpetas': subcarpetas,
        'pdfs': pdfs
    })
@login_required
def subir_pdf(request, carpeta_id):
    carpeta = get_object_or_404(Carpeta, id=carpeta_id)
    if request.method == 'POST':
        form = PDFForm(request.POST, request.FILES)
        if form.is_valid():
            pdf = form.save(commit=False)
            pdf.carpeta = carpeta
            pdf.save()
            return redirect('jugadores:detalle_carpeta', carpeta_id=carpeta.id)
    else:
        form = PDFForm()
    return render(request, 'jugadores/subir_pdf.html', {'form': form, 'carpeta': carpeta})
@login_required
def editar_jugador(request, jugador_id):
    jugador = get_object_or_404(Jugador, id=jugador_id)

    if request.method == 'POST':
        form = JugadorForm(request.POST, request.FILES, instance=jugador)
        perfil_pdf = request.FILES.get('perfil_pdf')

        if form.is_valid():
            form.save()
            if perfil_pdf:
                # Guarda el PDF como quieras. Este es solo un ejemplo:
                pdf = PDF(archivo=perfil_pdf, jugador=jugador)
                pdf.save()
            return redirect('jugadores:detalle_jugador', jugador_id=jugador.id)
    else:
        form = JugadorForm(instance=jugador)

    context = {
        'form': form,
        'jugador': jugador
    }

    return render(request, 'jugadores/editar_jugador.html', context)
@login_required
def eliminar_jugador(request, jugador_id):
    jugador = get_object_or_404(Jugador, id=jugador_id)

    if request.method == 'POST':
        jugador.delete()  # Esto también eliminará carpetas y PDFs porque están relacionados con `on_delete=models.CASCADE`
        return redirect('jugadores:lista_jugadores')

    return render(request, 'jugadores/eliminar_jugador.html', {'jugador': jugador})
@login_required
def editar_jugador(request, jugador_id):
    jugador = get_object_or_404(Jugador, id=jugador_id)
    
    if request.method == 'POST':
        form = JugadorForm(request.POST, instance=jugador)
        if form.is_valid():
            form.save()
            return redirect('jugadores:detalle_jugador', jugador_id=jugador.id)
    else:
        form = JugadorForm(instance=jugador)
    
    context = {
        'form': form,
        'jugador': jugador
    }
    
    return render(request, 'jugadores/editar_jugador.html', context)
@login_required
def eliminar_subcarpeta(request, subcarpeta_id):
    subcarpeta = get_object_or_404(Carpeta, id=subcarpeta_id)
    carpeta_id = subcarpeta.carpeta_padre.id  # Guarda la carpeta padre para redirigir después

    if request.method == 'POST':
        subcarpeta.delete()
        messages.success(request, 'Subcarpeta eliminada exitosamente.')
        return redirect('jugadores:detalle_carpeta', carpeta_id=carpeta_id)

    return render(request, 'jugadores/eliminar_subcarpeta.html', {'subcarpeta': subcarpeta})

@login_required
def eliminar_pdf(request, pdf_id):
    pdf = get_object_or_404(PDF, id=pdf_id)
    carpeta = pdf.carpeta  # Guarda la carpeta del PDF antes de borrarlo
    pdf.delete()
    messages.success(request, 'El archivo PDF ha sido eliminado exitosamente.')
    return redirect('jugadores:detalle_carpeta', carpeta.id)
@login_required
def eliminar_carpeta(request, carpeta_id):
    carpeta = get_object_or_404(Carpeta, id=carpeta_id)
    jugador_id = carpeta.jugador.id  # Para redirigir al detalle del jugador
    carpeta.delete()
    messages.success(request, 'Carpeta eliminada exitosamente.')
    return redirect('jugadores:detalle_jugador', jugador_id=jugador_id)
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('jugadores:lista_jugadores')  # Redirige a la lista de jugadores
        else:
            return render(request, 'jugadores/login.html', {'error': 'Credenciales inválidas'})
    return render(request, 'jugadores/login.html')

# jugadores/views.py

def logout_view(request):
    logout(request)
    return redirect('jugadores:login')  # Redirige a la página de login tras cerrar sesión
