# jugadores/models.py

from django.db import models

class Jugador(models.Model):
    nombre = models.CharField(max_length=100)
    equipo = models.CharField(max_length=100)
    categoria = models.CharField(max_length=50, null=True)
    ano = models.DateField()
    posicion = models.CharField(max_length=100)
    trayectoria = models.TextField(max_length=200)
    pais = models.CharField(max_length=20)
    seleccion = models.CharField(max_length=300, blank=True)
    img1 = models.ImageField(upload_to='covers/', blank=True, null=True)
    img2 = models.ImageField(upload_to='covers/', blank=True, null=True)
    img3 = models.ImageField(upload_to='covers/', blank=True, null=True)
    def __str__(self):
        return self.nombre

class Carpeta(models.Model):
    jugador = models.ForeignKey(Jugador, related_name='carpetas', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    carpeta_padre = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcarpetas')

    def __str__(self):
        return f"{self.nombre} - {self.jugador.nombre}"

class PDF(models.Model):
    carpeta = models.ForeignKey(Carpeta, related_name='pdfs', on_delete=models.CASCADE)
    archivo = models.FileField(upload_to='pdfs/')
    descripcion = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.archivo.name} - {self.carpeta.nombre}"
