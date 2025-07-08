from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sqlite3
from chart_generator import generar_grafica

app = Flask(__name__)
CORS(app)

# Página principal
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para obtener y registrar créditos
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
        return jsonify({"mensaje": "Crédito registrado con éxito"}), 201

    else:  # GET
        cursor.execute('SELECT * FROM creditos')
        creditos = cursor.fetchall()
        conn.close()
        return jsonify(creditos)
    
# Ruta para editar un crédito existente
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
    return jsonify({"mensaje": "Crédito actualizado correctamente"})

# Ruta para eliminar un crédito
@app.route('/api/creditos/<int:id>', methods=['DELETE'])
def eliminar_credito(id):
    conn = sqlite3.connect('creditos.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM creditos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({"mensaje": "Crédito eliminado correctamente"})
    

# Ruta para generar y mostrar la gráfica
@app.route('/grafica')
def grafica():
    return generar_grafica()

if __name__ == '__main__':
    app.run(debug=True)
