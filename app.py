import matplotlib
matplotlib.use('Agg')  # <-- Esto es clave, debe ir antes de pyplot
import matplotlib.pyplot as plt
from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS
import sqlite3
import os
from collections import defaultdict

app = Flask(__name__)
CORS(app)

# Conexión a la base de datos
def get_db_connection():
    conn = sqlite3.connect('creditos.db')
    conn.row_factory = sqlite3.Row
    return conn

# Generar gráfica 1: total de créditos otorgados por cliente
def generar_grafica_total_creditos():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT cliente FROM creditos')
    registros = cursor.fetchall()
    conn.close()

    if not registros:
        plt.figure(figsize=(10, 6))
        plt.text(0.5, 0.5, 'No hay datos para mostrar', ha='center', va='center', fontsize=14)
        plt.axis('off')
    else:
        conteo_por_cliente = defaultdict(int)
        for r in registros:
            conteo_por_cliente[r['cliente']] += 1

        clientes = list(conteo_por_cliente.keys())
        total_creditos = list(conteo_por_cliente.values())

        plt.figure(figsize=(10, 6))
        barras = plt.bar(clientes, total_creditos, color='#2ecc71')
        plt.title('Total de Créditos Otorgados por Cliente')
        plt.xlabel('Cliente')
        plt.ylabel('Cantidad de Créditos')
        plt.xticks(rotation=45)

        for barra in barras:
            altura = barra.get_height()
            plt.text(barra.get_x() + barra.get_width()/2, altura + 0.1, f'{int(altura)}', ha='center', va='bottom', fontsize=12)

        plt.tight_layout()

    path = os.path.join('static', 'grafica_total.png')
    plt.savefig(path)
    plt.close()

# Generar gráfica 2: distribución por rango de montos - CAMBIADA A BARRAS
def generar_grafica_por_rango():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT monto FROM creditos')
    registros = cursor.fetchall()
    conn.close()

    if not registros:
        plt.figure(figsize=(10, 6))
        plt.text(0.5, 0.5, 'No hay datos para mostrar', ha='center', va='center', fontsize=14)
        plt.axis('off')
    else:
        rangos = {'< $10,000': 0, '$10,000 - $30,000': 0, '> $30,000': 0}

        for r in registros:
            monto = r['monto']
            if monto < 10000:
                rangos['< $10,000'] += 1
            elif 10000 <= monto <= 30000:
                rangos['$10,000 - $30,000'] += 1
            else:
                rangos['> $30,000'] += 1

        labels = list(rangos.keys())
        valores = list(rangos.values())

        plt.figure(figsize=(10, 6))
        barras = plt.bar(labels, valores, color='#3498db')
        plt.title('Distribución de Créditos por Rango de Monto')
        plt.xlabel('Rango de Monto')
        plt.ylabel('Cantidad de Créditos')
        plt.xticks(rotation=0)

        for barra in barras:
            altura = barra.get_height()
            plt.text(barra.get_x() + barra.get_width()/2, altura + 0.1, f'{int(altura)}', ha='center', va='bottom', fontsize=12)

        plt.tight_layout()

    path = os.path.join('static', 'grafica2.png')
    plt.savefig(path)
    plt.close()

# Página principal
@app.route('/')
def index():
    return render_template('index.html')

# API para manejar créditos
@app.route('/api/creditos', methods=['GET', 'POST'])
def manejar_creditos():
    conn = sqlite3.connect('creditos.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        data = request.get_json()
        cursor.execute('''
            INSERT INTO creditos (cliente, monto, tasa, plazo, fecha, notas)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            data['cliente'],
            float(data['monto']),
            float(data['tasa']),
            int(data['plazo']),
            data['fecha'],
            data['notas']
        ))
        conn.commit()
        conn.close()

        # Regenerar imágenes
        generar_grafica_total_creditos()
        generar_grafica_por_rango()

        return jsonify({"mensaje": "Crédito registrado con éxito"}), 201

    else:
        cursor.execute('SELECT * FROM creditos')
        creditos = cursor.fetchall()
        conn.close()
        return jsonify(creditos)

# Editar crédito
@app.route('/api/creditos/<int:id>', methods=['PUT'])
def actualizar_credito(id):
    data = request.get_json()
    conn = sqlite3.connect('creditos.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE creditos
        SET cliente = ?, monto = ?, tasa = ?, plazo = ?, fecha = ?, notas = ?
        WHERE id = ?
    ''', (
        data['cliente'],
        float(data['monto']),
        float(data['tasa']),
        int(data['plazo']),
        data['fecha'],
        data['notas'],
        id
    ))
    conn.commit()
    conn.close()

    generar_grafica_total_creditos()
    generar_grafica_por_rango()

    return jsonify({"mensaje": "Crédito actualizado correctamente"})

# Eliminar crédito
@app.route('/api/creditos/<int:id>', methods=['DELETE'])
def eliminar_credito(id):
    conn = sqlite3.connect('creditos.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM creditos WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    generar_grafica_total_creditos()
    generar_grafica_por_rango()

    return jsonify({"mensaje": "Crédito eliminado correctamente"})

# Ruta para servir imagen gráfica total
@app.route('/grafica')
def mostrar_grafica_total():
    path = os.path.join('static', 'grafica_total.png')
    if not os.path.exists(path):
        generar_grafica_total_creditos()
    return send_file(path, mimetype='image/png')

# Ruta para servir imagen gráfica por rango
@app.route('/grafica2')
def mostrar_grafica_por_rango():
    path = os.path.join('static', 'grafica2.png')
    if not os.path.exists(path):
        generar_grafica_por_rango()
    return send_file(path, mimetype='image/png')

if __name__ == '__main__':
    # Generar las gráficas inicialmente
    generar_grafica_total_creditos()
    generar_grafica_por_rango()

    app.run(debug=True)
