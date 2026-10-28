
import sqlite3
import os

# ==========================================
# CONFIGURACIÓN DE LA BASE DE DATOS
# ==========================================

DB = "database/alumnos.db"


def conectar():
    os.makedirs("database", exist_ok=True)
    return sqlite3.connect(DB)


# ==========================================
# CREACIÓN DE LA BASE DE DATOS
# ==========================================

def crear_bd():
    conexion = conectar()
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


# ==========================================
# 1. ALTAS DE ALUMNOS
# ==========================================

def alta_alumno():
    print("\n===== ALTA DE ALUMNO =====")

    matricula = input("Matrícula: ").strip()
    nombre = input("Nombre: ").strip()
    apellido = input("Apellido: ").strip()
    calle = input("Calle: ").strip()
    colonia = input("Colonia: ").strip()
    padre_tutor = input("Padre o tutor: ").strip()
    tel_tutor = input("Teléfono del tutor: ").strip()

    if not matricula or not nombre or not apellido:
        print("La matrícula, el nombre y el apellido son obligatorios.")
        return

    conexion = conectar()

    try:
        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO alumno (
                matricula, nombre, apellido, calle,
                colonia, padre_tutor, tel_tutor
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            matricula, nombre, apellido, calle,
            colonia, padre_tutor, tel_tutor
        ))

        conexion.commit()
        print("\nAlumno registrado correctamente.")

    except sqlite3.IntegrityError:
        print("\nError: la matrícula ya existe.")

    except sqlite3.Error as error:
        print("Error al registrar al alumno:", error)

    finally:
        conexion.close()


# ==========================================
# 2. BAJAS DE ALUMNOS
# ==========================================

def baja_alumno():
    print("\n===== BAJA DE ALUMNO =====")

    matricula = input("Matrícula del alumno: ").strip()

    conexion = conectar()

    try:
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT * FROM alumno
            WHERE matricula = ?
        """, (matricula,))

        alumno = cursor.fetchone()

        if alumno is None:
            print("No se encontró un alumno con esa matrícula.")
            return

        print("\nDatos del alumno:")
        print("Matrícula:", alumno[0])
        print("Nombre:", alumno[1])
        print("Apellido:", alumno[2])
        print("Calle:", alumno[3])
        print("Colonia:", alumno[4])
        print("Padre o tutor:", alumno[5])
        print("Teléfono del tutor:", alumno[6])

        confirmacion = input(
            "\n¿Desea eliminar este alumno? (S/N): "
        ).strip().upper()

        if confirmacion == "S":
            cursor.execute("""
                DELETE FROM alumno
                WHERE matricula = ?
            """, (matricula,))

            conexion.commit()
            print("Alumno eliminado correctamente.")
        else:
            print("Operación cancelada.")

    except sqlite3.Error as error:
        print("Error al eliminar al alumno:", error)

    finally:
        conexion.close()


# ==========================================
# 3. MODIFICACIONES DE ALUMNOS
# ==========================================

def modificar_alumno():
    print("\n===== MODIFICACIÓN DE ALUMNO =====")

    matricula = input("Matrícula del alumno: ").strip()

    conexion = conectar()

    try:
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT nombre, apellido, calle, colonia,
                   padre_tutor, tel_tutor
            FROM alumno
            WHERE matricula = ?
        """, (matricula,))

        alumno = cursor.fetchone()

        if alumno is None:
            print("No se encontró un alumno con esa matrícula.")
            return

        print("\nIngrese los nuevos datos.")
        print("Presione ENTER para conservar el dato actual.")

        nombre = input(f"Nombre [{alumno[0]}]: ").strip()
        apellido = input(f"Apellido [{alumno[1]}]: ").strip()
        calle = input(f"Calle [{alumno[2] or ''}]: ").strip()
        colonia = input(f"Colonia [{alumno[3] or ''}]: ").strip()
        padre_tutor = input(
            f"Padre o tutor [{alumno[4] or ''}]: "
        ).strip()
        tel_tutor = input(
            f"Teléfono [{alumno[5] or ''}]: "
        ).strip()

        # Conservar los valores anteriores cuando se pulsa ENTER
        nombre = nombre or alumno[0]
        apellido = apellido or alumno[1]
        calle = calle or alumno[2] or ""
        colonia = colonia or alumno[3] or ""
        padre_tutor = padre_tutor or alumno[4] or ""
        tel_tutor = tel_tutor or alumno[5] or ""

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
            nombre, apellido, calle, colonia,
            padre_tutor, tel_tutor, matricula
        ))

        conexion.commit()
        print("\nAlumno modificado correctamente.")

    except sqlite3.Error as error:
        conexion.rollback()
        print("Error al modificar al alumno:", error)

    finally:
        conexion.close()


# ==========================================
# 4. CONSULTA DE TODA LA TABLA
# ==========================================

def consultar_todos():
    print("\n===== LISTADO DE ALUMNOS =====")

    conexion = conectar()

    try:
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT matricula, nombre, apellido, calle,
                   colonia, padre_tutor, tel_tutor
            FROM alumno
            ORDER BY apellido, nombre
        """)

        alumnos = cursor.fetchall()

        if not alumnos:
            print("No hay alumnos registrados.")
            return

        for alumno in alumnos:
            print("-" * 50)
            print("Matrícula:", alumno[0])
            print("Nombre:", alumno[1])
            print("Apellido:", alumno[2])
            print("Calle:", alumno[3] or "")
            print("Colonia:", alumno[4] or "")
            print("Padre o tutor:", alumno[5] or "")
            print("Teléfono del tutor:", alumno[6] or "")

        print("-" * 50)
        print("Total de alumnos:", len(alumnos))

    except sqlite3.Error as error:
        print("Error al consultar los alumnos:", error)

    finally:
        conexion.close()


# ==========================================
# 5. CONSULTA POR MATRÍCULA
# ==========================================

def consultar_matricula():
    print("\n===== CONSULTA POR MATRÍCULA =====")

    matricula = input("Ingrese la matrícula: ").strip()

    conexion = conectar()

    try:
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT matricula, nombre, apellido, calle,
                   colonia, padre_tutor, tel_tutor
            FROM alumno
            WHERE matricula = ?
        """, (matricula,))

        alumno = cursor.fetchone()

        if alumno:
            print("\n===== DATOS DEL ALUMNO =====")
            print("Matrícula:", alumno[0])
            print("Nombre:", alumno[1])
            print("Apellido:", alumno[2])
            print("Calle:", alumno[3] or "")
            print("Colonia:", alumno[4] or "")
            print("Padre o tutor:", alumno[5] or "")
            print("Teléfono del tutor:", alumno[6] or "")
        else:
            print("No se encontró un alumno con esa matrícula.")

    except sqlite3.Error as error:
        print("Error al consultar al alumno:", error)

    finally:
        conexion.close()


# ==========================================
# 6. MENÚ PRINCIPAL
# ==========================================

def menu():
    while True:
        print("\n" + "=" * 45)
        print("       SISTEMA DE CONTROL DE ALUMNOS")
        print("=" * 45)
        print("1. Alta de alumnos")
        print("2. Baja de alumnos")
        print("3. Modificación de alumnos")
        print("4. Consulta de toda la tabla")
        print("5. Consulta por matrícula")
        print("6. Salir del sistema")
        print("=" * 45)

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            alta_alumno()

        elif opcion == "2":
            baja_alumno()

        elif opcion == "3":
            modificar_alumno()

        elif opcion == "4":
            consultar_todos()

        elif opcion == "5":
            consultar_matricula()

        elif opcion == "6":
            print("\nSaliendo del sistema...")
            print("Gracias por utilizar el sistema.")
            break

        else:
            print("\nOpción inválida. Seleccione del 1 al 6.")


# ==========================================
# INICIO DEL PROGRAMA
# ==========================================

if __name__ == "__main__":
    crear_bd()
    menu()
