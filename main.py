import sqlite3
from pathlib import Path

RUTA_BD = Path(__file__).with_name("inventario.db")


def crear_tabla():
    conexion = sqlite3.connect(RUTA_BD)
    try:
        conexion.execute("""
            CREATE TABLE IF NOT EXISTS equipos (
                id INTEGER PRIMARY KEY,
                tipo TEXT NOT NULL,
                marca TEXT NOT NULL,
                modelo TEXT NOT NULL,
                numero_serie TEXT NOT NULL UNIQUE,
                ubicacion TEXT NOT NULL,
                estado TEXT NOT NULL
            )
        """)
        conexion.commit()
    finally:
        conexion.close()


def registrar_equipo():
    campos = (
        ("tipo", "Tipo de equipo"),
        ("marca", "Marca"),
        ("modelo", "Modelo"),
        ("numero_serie", "Número de serie"),
        ("ubicacion", "Ubicación"),
        ("estado", "Estado"),
    )
    datos = []

    for campo, etiqueta in campos:
        valor = input(f"{etiqueta}: ").strip()

        while not valor:
            print("Este campo es obligatorio.")
            valor = input(f"{etiqueta}: ").strip()

        if campo == "numero_serie":
            valor = valor.upper()

        datos.append(valor)

    conexion = sqlite3.connect(RUTA_BD)
    try:
        conexion.execute("""
            INSERT INTO equipos
                (tipo, marca, modelo, numero_serie, ubicacion, estado)
            VALUES (?, ?, ?, ?, ?, ?)
        """, datos)
        conexion.commit()
        print("Equipo registrado correctamente.")
    except sqlite3.IntegrityError:
        print("No se pudo registrar: ya existe ese número de serie.")
    finally:
        conexion.close()


def listar_equipos():
    conexion = sqlite3.connect(RUTA_BD)
    try:
        equipos = conexion.execute("""
            SELECT id, tipo, marca, modelo, numero_serie, ubicacion, estado
            FROM equipos
            ORDER BY id
        """).fetchall()
    finally:
        conexion.close()

    if not equipos:
        print("Todavía no hay equipos registrados.")
        return

    print("\n--- EQUIPOS REGISTRADOS ---")

    for equipo in equipos:
        identificador, tipo, marca, modelo, serie, ubicacion, estado = equipo
        print(f"\nID: {identificador}")
        print(f"Equipo: {tipo} | {marca} | {modelo}")
        print(f"Número de serie: {serie}")
        print(f"Ubicación: {ubicacion}")
        print(f"Estado: {estado}")


def mostrar_menu():
    while True:
        print("\n--- INVENTARIO DEL COLEGIO ---")
        print("1. Registrar equipo")
        print("2. Listar equipos")
        print("3. Salir")

        opcion = input("Elige una opción: ").strip()

        if opcion == "1":
            registrar_equipo()
        elif opcion == "2":
            listar_equipos()
        elif opcion == "3":
            print("Programa cerrado.")
            break
        else:
            print("Opción inválida. Elige 1, 2 o 3.")


if __name__ == "__main__":
    crear_tabla()
    mostrar_menu()