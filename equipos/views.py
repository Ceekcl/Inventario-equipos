from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import render

from .models import Equipo


@staff_member_required
@permission_required("equipos.view_equipo", raise_exception=True)
def lista_equipos(request):
    busqueda = request.GET.get("q", "").strip()
    estado = request.GET.get("estado", "").strip()

    resumen = Equipo.objects.aggregate(
        total=Count("id"),
        operativos=Count(
            "id",
            filter=Q(estado=Equipo.Estado.OPERATIVO),
        ),
        en_reparacion=Count(
            "id",
            filter=Q(estado=Equipo.Estado.EN_REPARACION),
        ),
        dados_de_baja=Count(
            "id",
            filter=Q(estado=Equipo.Estado.DADO_DE_BAJA),
        ),
    )

    equipos = Equipo.objects.all()

    if busqueda:
        equipos = equipos.filter(
            Q(numero_serie__icontains=busqueda)
            | Q(tipo__icontains=busqueda)
            | Q(marca__icontains=busqueda)
            | Q(modelo__icontains=busqueda)
            | Q(ubicacion__icontains=busqueda)
        )

    if estado in Equipo.Estado.values:
        equipos = equipos.filter(estado=estado)
    else:
        estado = ""

    pagina = Paginator(
        equipos.order_by("numero_serie"), 20
    ).get_page(request.GET.get("page"))

    return render(
        request,
        "equipos/lista.html",
        {
            "pagina": pagina,
            "busqueda": busqueda,
            "estado_actual": estado,
            "estados": Equipo.Estado.choices,
            "resumen": resumen,
        },
    )