from django.contrib import admin
from django.urls import path

from equipos.views import lista_equipos

urlpatterns = [
    path("", lista_equipos, name="lista_equipos"),
    path("admin/", admin.site.urls),
]