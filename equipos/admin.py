from django.contrib import admin

from .models import Equipo


@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    list_display = (
        "numero_serie",
        "tipo",
        "marca",
        "modelo",
        "ubicacion",
        "estado",
    )
    search_fields = (
        "numero_serie",
        "marca",
        "modelo",
        "ubicacion",
    )
    list_filter = ("estado", "tipo", "ubicacion")
    ordering = ("numero_serie",)
    list_per_page = 25


admin.site.site_header = "Inventario escolar"
admin.site.site_title = "Inventario escolar"
admin.site.index_title = "Administración de equipos"