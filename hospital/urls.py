from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from hospital import views

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', views.isActivatedView, name="Create"),
    #path('pdf/', views.some_view, name="pdf"),
    
    path('create/', views.create, name="Create"),    
    path('listado/', views.listado, name="List"),
    path('listado/alfa', views.listado_alf, name="ListAlfa"),

    path('listado/porAnio', views.listado_porAnio, name="ListPorAnio"),
    path('listado/buscarPorDNI', views.buscarPorDNI, name="buscarDNI"),
    path('listado/buscarPorNombre', views.buscarPorNombre, name="buscarNombre"),
    path('Nueva-Obra-Social/', views.NewOS , name="NewOS"),
    path('Nueva-Escuela/', views.NewEsc, name="NewEsc"),
]

handler404="hospital.views.handle_not_found"
