import sqlite3
from pathlib import Path

RUTA_BD = Path(__file__).with_name("inventario.db")
ESTADOS = ("Operativo", "En reparación", "Dado de baja")


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


def pedir_texto(etiqueta):
    while True:
        valor = input(f"{etiqueta}: ").strip()
        if valor:
            return valor
        print("Este campo es obligatorio.")


def elegir_estado():
    while True:
        print("\nEstados disponibles:")
        for numero, estado in enumerate(ESTADOS, start=1):
            print(f"{numero}. {estado}")

        opcion = input("Elige un estado: ").strip()

        if opcion in ("1", "2", "3"):
            return ESTADOS[int(opcion) - 1]

        print("Opción inválida. Elige 1, 2 o 3.")


def mostrar_equipo(equipo):
    identificador, tipo, marca, modelo, serie, ubicacion, estado = equipo
    print(f"\nID: {identificador}")
    print(f"Equipo: {tipo} | {marca} | {modelo}")
    print(f"Número de serie: {serie}")
    print(f"Ubicación: {ubicacion}")
    print(f"Estado: {estado}")


def obtener_equipo(serie):
    conexion = sqlite3.connect(RUTA_BD)
    try:
        return conexion.execute("""
            SELECT id, tipo, marca, modelo, numero_serie, ubicacion, estado
            FROM equipos
            WHERE numero_serie = ?
        """, (serie,)).fetchone()
    finally:
        conexion.close()


def registrar_equipo():
    tipo = pedir_texto("Tipo de equipo")
    marca = pedir_texto("Marca")
    modelo = pedir_texto("Modelo")
    serie = pedir_texto("Número de serie").upper()
    ubicacion = pedir_texto("Ubicación")
    estado = elegir_estado()

    conexion = sqlite3.connect(RUTA_BD)
    try:
        conexion.execute("""
            INSERT INTO equipos
                (tipo, marca, modelo, numero_serie, ubicacion, estado)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (tipo, marca, modelo, serie, ubicacion, estado))
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
        mostrar_equipo(equipo)


def buscar_equipo():
    serie = pedir_texto("Número de serie que deseas buscar").upper()
    equipo = obtener_equipo(serie)

    if equipo is None:
        print("No se encontró un equipo con ese número de serie.")
        return

    print("\n--- EQUIPO ENCONTRADO ---")
    mostrar_equipo(equipo)


def actualizar_estado():
    serie = pedir_texto("Número de serie del equipo").upper()
    equipo = obtener_equipo(serie)

    if equipo is None:
        print("No se encontró un equipo con ese número de serie.")
        return

    print("\n--- EQUIPO A ACTUALIZAR ---")
    mostrar_equipo(equipo)
    nuevo_estado = elegir_estado()

    if nuevo_estado == equipo[6]:
        print("El equipo ya tiene ese estado.")
        return

    confirmacion = input(
        f"¿Cambiar el estado a '{nuevo_estado}'? (s/n): "
    ).strip().lower()

    if confirmacion != "s":
        print("Cambio cancelado.")
        return

    conexion = sqlite3.connect(RUTA_BD)
    try:
        conexion.execute("""
            UPDATE equipos
            SET estado = ?
            WHERE numero_serie = ?
        """, (nuevo_estado, serie))
        conexion.commit()
        print("Estado actualizado correctamente.")
    finally:
        conexion.close()


def mostrar_menu():
    while True:
        print("\n--- INVENTARIO DEL COLEGIO ---")
        print("1. Registrar equipo")
        print("2. Listar equipos")
        print("3. Buscar por número de serie")
        print("4. Actualizar estado")
        print("5. Salir")

        opcion = input("Elige una opción: ").strip()

        if opcion == "1":
            registrar_equipo()
        elif opcion == "2":
            listar_equipos()
        elif opcion == "3":
            buscar_equipo()
        elif opcion == "4":
            actualizar_estado()
        elif opcion == "5":
            print("Programa cerrado.")
            break
        else:
            print("Opción inválida. Elige un número del 1 al 5.")


if __name__ == "__main__":
    crear_tabla()
    mostrar_menu()
    