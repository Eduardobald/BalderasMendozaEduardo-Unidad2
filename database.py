
import sqlite3

def crear_bd():
    conexion = sqlite3.connect("materiales.db")
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS materiales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT NOT NULL,
            proveedor TEXT NOT NULL,
            material TEXT NOT NULL,
            cantidad REAL NOT NULL
        )
    """)

    conexion.commit()
    conexion.close()

if __name__ == "__main__":
    crear_bd()

    