from flask import Flask, redirect, url_for, render_template, request, flash
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

    clientes = conn.execute(
        'SELECT * FROM clientes'
    ).fetchall()

    conn.close()

    return render_template(
        'clientes.html',
        clientes=clientes
    )


@app.route('/agregar_cliente', methods=['GET', 'POST'])
def agregar_cliente():

    if request.method == 'POST':

        nombre = request.form['nombre']
        email = request.form['email']

        conn = get_db_connection()

        conn.execute(
            'INSERT INTO clientes (nombre, email) VALUES (?, ?)',
            (nombre, email)
        )

        conn.commit()
        conn.close()

        flash('Cliente agregado exitosamente.')

        return redirect(url_for('clientes'))

    return render_template(
        'form_cliente.html',
        cliente=None
    )


@app.route('/editar_cliente/<int:id>', methods=['GET', 'POST'])
def editar_cliente(id):

    conn = get_db_connection()

    cliente = conn.execute(
        'SELECT * FROM clientes WHERE id = ?',
        (id,)
    ).fetchone()

    if request.method == 'POST':

        nombre = request.form['nombre']
        email = request.form['email']

        conn.execute(
            '''
            UPDATE clientes
            SET nombre = ?, email = ?
            WHERE id = ?
            ''',
            (nombre, email, id)
        )

        conn.commit()
        conn.close()

        flash('Cliente editado exitosamente.')

        return redirect(url_for('clientes'))

    conn.close()

    return render_template(
        'form_cliente.html',
        cliente=cliente
    )


@app.route('/eliminar_cliente/<int:id>', methods=['GET', 'POST'])
def eliminar_cliente(id):

    conn = get_db_connection()

    conn.execute(
        'DELETE FROM clientes WHERE id = ?',
        (id,)
    )

    conn.commit()
    conn.close()

    flash('Cliente eliminado exitosamente.')

    return redirect(url_for('clientes'))



@app.route('/categoria')
def categoria():

    conn = get_db_connection()

    categorias = conn.execute(
        'SELECT * FROM categoria'
    ).fetchall()

    conn.close()

    return render_template(
        'categoria.html',
        categorias=categorias
    )


@app.route('/agregar_categoria', methods=['GET', 'POST'])
def agregar_categoria():

    if request.method == 'POST':

        nombre = request.form['nombre']

        conn = get_db_connection()

        conn.execute(
            'INSERT INTO categoria (nombre) VALUES (?)',
            (nombre,)
        )

        conn.commit()
        conn.close()

        flash('Categoría agregada exitosamente.')

        return redirect(url_for('categoria'))

    return render_template(
        'form_categoria.html',
        categoria=None
    )


@app.route('/editar_categoria/<int:id>', methods=['GET', 'POST'])
def editar_categoria(id):

    conn = get_db_connection()

    categoria = conn.execute(
        'SELECT * FROM categoria WHERE id = ?',
        (id,)
    ).fetchone()

    if request.method == 'POST':

        nombre = request.form['nombre']

        conn.execute(
            '''
            UPDATE categoria
            SET nombre = ?
            WHERE id = ?
            ''',
            (nombre, id)
        )

        conn.commit()
        conn.close()

        flash('Categoría editada exitosamente.')

        return redirect(url_for('categoria'))

    conn.close()

    return render_template(
        'form_categoria.html',
        categoria=categoria
    )


@app.route('/eliminar_categoria/<int:id>', methods=['GET', 'POST'])
def eliminar_categoria(id):

    conn = get_db_connection()

    conn.execute(
        'DELETE FROM categoria WHERE id = ?',
        (id,)
    )

    conn.commit()
    conn.close()

    flash('Categoría eliminada exitosamente.')

    return redirect(url_for('categoria'))



@app.route('/compras')
def compras():

    conn = get_db_connection()

    compras = conn.execute(
        '''
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
        '''
    ).fetchall()

    conn.close()

    return render_template(
        'compras.html',
        compras=compras
    )


@app.route('/agregar_compra', methods=['GET', 'POST'])
def agregar_compra():

    conn = get_db_connection()

    clientes = conn.execute(
        'SELECT * FROM clientes'
    ).fetchall()

    categorias = conn.execute(
        'SELECT * FROM categoria'
    ).fetchall()

    if request.method == 'POST':

        cliente_id = request.form['cliente_id']
        categoria_id = request.form['categoria_id']
        fecha = request.form['fecha']

        conn.execute(
            '''
            INSERT INTO compras
            (cliente_id, categoria_id, fecha)
            VALUES (?, ?, ?)
            ''',
            (cliente_id, categoria_id, fecha)
        )

        conn.commit()
        conn.close()

        flash('Compra agregada exitosamente.')

        return redirect(url_for('compras'))

    conn.close()

    return render_template(
        'form_compra.html',
        compra=None,
        clientes=clientes,
        categorias=categorias
    )


@app.route('/editar_compra/<int:id>', methods=['GET', 'POST'])
def editar_compra(id):

    conn = get_db_connection()

    compra = conn.execute(
        '''
        SELECT *
        FROM compras
        WHERE id = ?
        ''',
        (id,)
    ).fetchone()

    clientes = conn.execute(
        'SELECT * FROM clientes'
    ).fetchall()

    categorias = conn.execute(
        'SELECT * FROM categoria'
    ).fetchall()

    if request.method == 'POST':

        cliente_id = request.form['cliente_id']
        categoria_id = request.form['categoria_id']
        fecha = request.form['fecha']

        conn.execute(
            '''
            UPDATE compras
            SET cliente_id = ?,
                categoria_id = ?,
                fecha = ?
            WHERE id = ?
            ''',
            (cliente_id, categoria_id, fecha, id)
        )

        conn.commit()
        conn.close()

        flash('Compra editada exitosamente.')

        return redirect(url_for('compras'))

    conn.close()

    return render_template(
        'form_compra.html',
        compra=compra,
        clientes=clientes,
        categorias=categorias
    )


@app.route('/eliminar_compra/<int:id>', methods=['GET', 'POST'])
def eliminar_compra(id):

    conn = get_db_connection()

    conn.execute(
        'DELETE FROM compras WHERE id = ?',
        (id,)
    )

    conn.commit()
    conn.close()

    flash('Compra eliminada exitosamente.')

    return redirect(url_for('compras'))


if __name__ == '__main__':
    app.run(debug=True)