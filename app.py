
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from database import crear_bd

app = Flask(__name__)

crear_bd()


def conectar_bd():
    conexion = sqlite3.connect("materiales.db")
    conexion.row_factory = sqlite3.Row
    return conexion


@app.route("/")
def inicio():
    conexion = conectar_bd()

    materiales = conexion.execute(
        "SELECT * FROM materiales ORDER BY id DESC"
    ).fetchall()

    total_registros = conexion.execute(
        "SELECT COUNT(*) FROM materiales"
    ).fetchone()[0]

    total_kg = conexion.execute(
        "SELECT COALESCE(SUM(cantidad), 0) FROM materiales"
    ).fetchone()[0]

    total_tipos = conexion.execute(
        "SELECT COUNT(DISTINCT material) FROM materiales"
    ).fetchone()[0]

    conexion.close()

    return render_template(
        "index.html",
        materiales=materiales,
        total_registros=total_registros,
        total_kg=total_kg,
        total_tipos=total_tipos
    )


@app.route("/registrar", methods=["POST"])
def registrar():
    fecha = request.form["fecha"]
    proveedor = request.form["proveedor"]
    material = request.form["material"]
    cantidad = request.form["cantidad"]

    conexion = conectar_bd()

    conexion.execute("""
        INSERT INTO materiales
        (fecha, proveedor, material, cantidad)
        VALUES (?, ?, ?, ?)
    """, (fecha, proveedor, material, cantidad))

    conexion.commit()
    conexion.close()

    return redirect(url_for("inicio"))


@app.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    conexion = conectar_bd()

    conexion.execute(
        "DELETE FROM materiales WHERE id = ?",
        (id,)
    )

    conexion.commit()
    conexion.close()

    return redirect(url_for("inicio"))


if __name__ == "__main__":
    app.run(debug=True)
