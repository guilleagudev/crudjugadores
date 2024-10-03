# jugadores/forms.py

from django import forms
from .models import Jugador, Carpeta, PDF
from django.contrib.auth.forms import AuthenticationForm

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(label='Usuario', max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa tu usuario'}))
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa tu contraseña'}))
class JugadorForm(forms.ModelForm):
    class Meta:
        model = Jugador
        fields = ['nombre','equipo', 'categoria', 'ano', 'posicion', 'trayectoria', 'pais', 'seleccion', 'img1' ]

class CarpetaForm(forms.ModelForm):
    class Meta:
        model = Carpeta
        fields = ['nombre']

class PDFForm(forms.ModelForm):
    class Meta:
        model = PDF
        fields = ['archivo', 'descripcion']

class JugadorSearchForm(forms.Form):
    nombre = forms.CharField(required=False, label='Nombre')
    equipo = forms.CharField(required=False, label='Equipo')
    categoria = forms.CharField(required=False, label='Categoría')
    ano = forms.IntegerField(required=False, label='Año')
    posicion = forms.CharField(required=False, label='Posición')
    trayectoria = forms.CharField(
        required=False,
        label='Trayectoria',
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Describe la trayectoria del jugador...'})
    )
    pais = forms.CharField(required=False, label='País')