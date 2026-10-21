import os
import sqlite3
from pathlib import Path

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import DatabaseError, transaction

from equipos.models import Equipo


def importar():
    origen = Path(__file__).resolve().with_name("inventario.db")
    destino = Path(settings.DATABASES["default"]["NAME"]).resolve()

    if not origen.is_file():
        print("No se encontró inventario.db junto a este archivo.")
        return

    if origen == destino:
        print("La base de origen y la de destino deben ser diferentes.")
        return

    # Abre la base anterior únicamente para lectura.
    conexion = sqlite3.connect(origen.as_uri() + "?mode=ro", uri=True)
    conexion.row_factory = sqlite3.Row

    try:
        filas = conexion.execute("""
            SELECT tipo, marca, modelo, numero_serie, ubicacion, estado
            FROM equipos
            ORDER BY id
        """).fetchall()
    finally:
        conexion.close()

    creados = 0
    omitidos = 0
    serie = ""

    try:
        with transaction.atomic():
            for fila in filas:
                datos = {
                    campo: valor.strip() if isinstance(valor, str) else valor
                    for campo, valor in dict(fila).items()
                }
                serie = (datos["numero_serie"] or "").upper()
                datos["numero_serie"] = serie

                if Equipo.objects.filter(
                    numero_serie__iexact=serie
                ).exists():
                    omitidos += 1
                    continue

                equipo = Equipo(**datos)
                equipo.full_clean()
                equipo.save()
                creados += 1

    except ValidationError as error:
        print(f"Revisa los datos del equipo con serie: {serie}")
        print(error.message_dict)
        print("La importación se canceló sin guardar equipos nuevos.")
        return

    print("Importación terminada.")
    print(f"Equipos nuevos importados: {creados}")
    print(f"Series ya existentes, conservadas sin cambios: {omitidos}")
    print("La base de datos original no fue modificada.")


if __name__ == "__main__":
    try:
        importar()
    except (sqlite3.Error, DatabaseError) as error:
        print(f"No se pudo completar la importación: {error}")