import sqlite3
import os

# ==========================================
# MÓDULO 1. CREACIÓN DE LA BASE DE DATOS
# ==========================================

def crear_bd():
    os.makedirs("database", exist_ok=True)

    conexion = sqlite3.connect("database/alumnos.db")
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alumno (
            matricula TEXT PRIMARY KEY,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            calle TEXT,
            colonia TEXT,
            padre_tutor TEXT,
            tel_tutor TEXT
        )
    """)

    conexion.commit()
    conexion.close()

    print("Base de datos creada correctamente.")
    print("Base de datos creada con exito")


# ==========================================
# MÓDULO 2. ALTAS DE ALUMNOS
# ==========================================

def alta_alumno():
    conexion = sqlite3.connect("database/alumnos.db")
    cursor = conexion.cursor()

    print("\n===== ALTA DE ALUMNO =====")

    matricula = input("Matrícula: ").strip()
    nombre = input("Nombre: ").strip()
    apellido = input("Apellido: ").strip()
    calle = input("Calle: ").strip()
    colonia = input("Colonia: ").strip()
    padre_tutor = input("Nombre del padre o tutor: ").strip()
    tel_tutor = input("Teléfono del tutor: ").strip()

    if not matricula or not nombre or not apellido:
        print("Error: matrícula, nombre y apellido son obligatorios.")
        conexion.close()
        return

    try:
        cursor.execute("""
            INSERT INTO alumno (
                matricula,
                nombre,
                apellido,
                calle,
                colonia,
                padre_tutor,
                tel_tutor
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            matricula,
            nombre,
            apellido,
            calle,
            colonia,
            padre_tutor,
            tel_tutor
        ))

        conexion.commit()
        print("Alumno registrado correctamente.")

    except sqlite3.IntegrityError:
        print("Error: la matrícula ya existe.")

    except sqlite3.Error as error:
        print(f"Error al registrar al alumno: {error}")

    finally:
        conexion.close()


# ==========================================
# PROGRAMA PRINCIPAL
# ==========================================

if __name__ == "__main__":
    crear_bd()
    alta_alumno()