from flask import Flask, redirect, url_for, render_template
import sqlite3

app = Flask(__name__)

app.secret_key = 'secreto'


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    return redirect(url_for('clientes'))


@app.route('/clientes')
def clientes():
    conn = get_db_connection()
    clientes = conn.execute('SELECT * FROM clientes').fetchall()
    conn.close()

    return render_template('clientes.html', clientes=clientes)


@app.route('/categoria')
def categoria():
    conn = get_db_connection()
    categorias = conn.execute('SELECT * FROM categoria').fetchall()
    conn.close()

    return render_template('categoria.html', categorias=categorias)


@app.route('/compras')
def compras():
    conn = get_db_connection()

    compras = conn.execute("""
        SELECT
            i.id,
            i.fecha,
            c.nombre AS cliente,
            p.nombre AS categoria
        FROM compras i
        JOIN clientes c
            ON i.cliente_id = c.id
        JOIN categoria p
            ON i.categoria_id = p.id
    """).fetchall()

    conn.close()

    return render_template('compras.html', compras=compras)
@app.route('/agregar_categoria', methods=['POST'])
def agregar_categoria():
    from flask import request
    nombre = request.form['nombre']
    conn = get_db_connection()
    conn.execute('INSERT INTO categoria (nombre) VALUES (?)', (nombre,))
    conn.commit()
    conn.close()
    return redirect(url_for('categoria'))


if __name__ == '__main__':
    app.run(debug=True)