# Generated by Django 5.1.1 on 2024-09-24 09:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Jugador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('equipo', models.CharField(max_length=100)),
                ('categoria', models.CharField(max_length=50, null=True)),
                ('ano', models.DateField()),
                ('posicion', models.CharField(max_length=100)),
                ('trayectoria', models.CharField(max_length=200)),
                ('pais', models.CharField(max_length=20)),
                ('seleccion', models.CharField(max_length=200, null=True)),
                ('img1', models.ImageField(blank=True, null=True, upload_to='covers/')),
                ('img2', models.ImageField(blank=True, null=True, upload_to='covers/')),
                ('img3', models.ImageField(blank=True, null=True, upload_to='covers/')),
            ],
        ),
        migrations.CreateModel(
            name='Carpeta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('jugador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='carpetas', to='jugadores.jugador')),
            ],
        ),
        migrations.CreateModel(
            name='PDF',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('archivo', models.FileField(upload_to='pdfs/')),
                ('descripcion', models.CharField(blank=True, max_length=255)),
                ('carpeta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pdfs', to='jugadores.carpeta')),
            ],
        ),
    ]
