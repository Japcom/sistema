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
# ======= Modulo de modificaciones
# ==========================================

def modificar_alumno():

    conexion = sqlite3.connect("database/alumnos.db")
    cursor = conexion.cursor()

    print("\n===== MODIFICACIÓN DE ALUMNO =====")

    matricula = input("Ingrese la matrícula del alumno: ").strip()

    # Buscar al alumno
    cursor.execute("""
        SELECT nombre, apellido, calle, colonia,
               padre_tutor, tel_tutor
        FROM alumno
        WHERE matricula = ?
    """, (matricula,))

    alumno = cursor.fetchone()

    if alumno is None:
        print("Error: no se encontró un alumno con esa matrícula.")
        conexion.close()
        return

    print("\nDatos actuales del alumno:")
    print("Nombre:", alumno[0])
    print("Apellido:", alumno[1])
    print("Calle:", alumno[2])
    print("Colonia:", alumno[3])
    print("Padre o tutor:", alumno[4])
    print("Teléfono del tutor:", alumno[5])

    print("\nIngrese los nuevos datos.")
    print("Presione ENTER para conservar el dato actual.")

    nombre = input(f"Nombre [{alumno[0]}]: ").strip()
    apellido = input(f"Apellido [{alumno[1]}]: ").strip()
    calle = input(f"Calle [{alumno[2]}]: ").strip()
    colonia = input(f"Colonia [{alumno[3]}]: ").strip()
    padre_tutor = input(
        f"Padre o tutor [{alumno[4]}]: "
    ).strip()
    tel_tutor = input(
        f"Teléfono del tutor [{alumno[5]}]: "
    ).strip()

    # Conservar los datos si no se ingresaron cambios
    nombre = nombre if nombre else alumno[0]
    apellido = apellido if apellido else alumno[1]
    calle = calle if calle else alumno[2]
    colonia = colonia if colonia else alumno[3]
    padre_tutor = padre_tutor if padre_tutor else alumno[4]
    tel_tutor = tel_tutor if tel_tutor else alumno[5]

    try:
        cursor.execute("""
            UPDATE alumno
            SET nombre = ?,
                apellido = ?,
                calle = ?,
                colonia = ?,
                padre_tutor = ?,
                tel_tutor = ?
            WHERE matricula = ?
        """, (
            nombre,
            apellido,
            calle,
            colonia,
            padre_tutor,
            tel_tutor,
            matricula
        ))

        conexion.commit()
        print("\nAlumno modificado correctamente.")

    except sqlite3.Error as error:
        conexion.rollback()
        print("Error al modificar el alumno:", error)

    finally:
        conexion.close()

# ==========================================
# PROGRAMA PRINCIPAL
# ==========================================

if __name__ == "__main__":
    crear_bd()
    alta_alumno()
    modificar_alumno()