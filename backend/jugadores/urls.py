# jugadores/urls.py

from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'jugadores'

urlpatterns = [
    path('', views.lista_jugadores, name='lista_jugadores'),
    path('jugador/nuevo/', views.crear_jugador, name='crear_jugador'),
    path('jugador/<int:jugador_id>/', views.detalle_jugador, name='detalle_jugador'),
    path('jugador/<int:jugador_id>/carpeta/nueva/', views.crear_carpeta, name='crear_carpeta'),
    path('carpeta/<int:carpeta_id>/', views.detalle_carpeta, name='detalle_carpeta'),
    path('carpeta/<int:carpeta_id>/pdf/nuevo/', views.subir_pdf, name='subir_pdf'),
    path('jugador/<int:jugador_id>/editar/', views.editar_jugador, name='editar_jugador'),
    path('jugador/<int:jugador_id>/eliminar/', views.eliminar_jugador, name='eliminar_jugador'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('pdf/eliminar/<int:pdf_id>/', views.eliminar_pdf, name='eliminar_pdf'),
    path('eliminar_carpeta/<int:carpeta_id>/', views.eliminar_carpeta, name='eliminar_carpeta'),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)