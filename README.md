# Inventario de equipos escolares

Aplicación de consola para registrar y consultar equipos tecnológicos de un colegio.

Proyecto de aprendizaje y portafolio desarrollado con Python y SQLite, inspirado en tareas de soporte TI escolar.

## Funcionalidades

- Registrar equipos con tipo, marca, modelo, número de serie, ubicación y estado.
- Listar los equipos registrados.
- Buscar un equipo por su número de serie.
- Actualizar el estado de un equipo con confirmación.
- Seleccionar estados: Operativo, En reparación o Dado de baja.
- Evitar números de serie duplicados.
- Rechazar campos vacíos al registrar.
- Conservar los datos entre ejecuciones mediante SQLite.

## Tecnologías

- Python 3.
- SQLite, mediante el módulo sqlite3.
- Git y GitHub para el control de versiones.

## Cómo ejecutar

Necesitas Python 3 con el módulo sqlite3 disponible.

1. Clona el repositorio:

   ```bash
   git clone https://github.com/Ceekcl/Inventario-equipos.git
   ```

2. Entra en la carpeta:

   ```bash
   cd Inventario-equipos
   ```

3. Ejecuta el programa:

   ```bash
   python main.py
   ```

   En Windows también puedes utilizar:

   ```bash
   py main.py
   ```

La base de datos inventario.db se crea automáticamente junto a main.py en la primera ejecución. No requiere configurar un servidor de base de datos.

## Estructura

- main.py: menú, validaciones y operaciones de la base de datos.
- README.md: descripción e instrucciones de uso.
- .gitignore: exclusiones para el control de versiones.
- inventario.db: base de datos local generada al ejecutar el programa; no se incluye en GitHub.

## Ejemplo de prueba

Puedes registrar un equipo ficticio con estos datos:

- Tipo: Notebook.
- Marca: Lenovo.
- Modelo: Equipo de prueba.
- Número de serie: DEMO-001.
- Ubicación: Sala de informática.
- Estado: Operativo.

Después puedes buscarlo, cambiar su estado y cerrar y abrir el programa para comprobar que el cambio se conserva.

## Comprobaciones manuales realizadas

- Registro de un equipo ficticio.
- Consulta del equipo mediante listado y búsqueda por serie.
- Actualización del estado a En reparación.
- Persistencia del estado después de reiniciar el programa.

## Próximas mejoras

- Agregar pruebas automatizadas.
- Filtrar equipos por ubicación y estado.
- Exportar el inventario a CSV.
- Registrar un historial de cambios de estado.
- Incorporar una interfaz gráfica o web.

## Alcance actual

Primera versión de consola para uso local y aprendizaje. No incluye autenticación, roles ni gestión de múltiples usuarios.

Para las demostraciones del portafolio se utilizan datos ficticios.