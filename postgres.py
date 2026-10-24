import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Configuración de credenciales de acceso (ajusta usuario, contraseña y puerto según tu entorno)
DB_HOST = "localhost"
DB_PORT = "5433"
DB_USER = "postgres"
DB_PASSWORD = "Conalep:169"  # Reemplaza con tu contraseña de PostgreSQL

def inicializar_base_de_datos():
    # PASO 1: Conectarse a la base de datos por defecto ('postgres') para crear la BD 'escuela'
    try:
        conexion = psycopg2.connect(
            host=DB_HOST,
            database="postgres",
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        
        # PostgreSQL no permite ejecutar 'CREATE DATABASE' dentro de un bloque de transacciones habitual.
        # Se requiere activar el modo autocommit.
        conexion.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conexion.cursor()

        # Intentar crear la base de datos 'escuela'
        try:
            cursor.execute("CREATE DATABASE escuela;")
            print("Base de datos 'escuela' creada exitosamente.")
        except psycopg2.errors.DuplicateDatabase:
            print("La base de datos 'escuela' ya existe. Omitiendo creación...")

        cursor.close()
        conexion.close()

    except Exception as error:
        print(f"Error en la conexión inicial o al crear la base de datos: {error}")
        return

    # PASO 2: Conectarse a la nueva base de datos 'escuela' para crear la tabla 'alumnos'
    try:
        conexion_escuela = psycopg2.connect(
            host=DB_HOST,
            database="escuela",
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        
        cursor_escuela = conexion_escuela.cursor()

        # Sentencia SQL para crear la tabla con los campos requeridos
        query_crear_tabla = """
        CREATE TABLE IF NOT EXISTS alumnos (
            matricula VARCHAR(20) PRIMARY KEY,
            nombre VARCHAR(50) NOT NULL,
            apellido VARCHAR(50) NOT NULL,
            calle VARCHAR(100),
            colonia VARCHAR(100),
            telefono VARCHAR(20)
        );
        """
        
        cursor_escuela.execute(query_crear_tabla)
        conexion_escuela.commit()
        print("Tabla 'alumnos' creada exitosamente dentro de la base de datos 'escuela'.")

        cursor_escuela.close()
        conexion_escuela.close()

    except Exception as error:
        print(f"Error al conectar a la base de datos 'escuela' o al crear la tabla: {error}")

if __name__ == "__main__":
    inicializar_base_de_datos()