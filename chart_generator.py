import sqlite3
import matplotlib.pyplot as plt
from flask import send_file
import os

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.size": 12
})

def generar_grafica():
    conn = sqlite3.connect("creditos.db")
    cursor = conn.cursor()
    cursor.execute("SELECT cliente, monto FROM creditos")
    data = cursor.fetchall()
    conn.close()

    plt.figure(figsize=(10, 5))
    ax = plt.gca()
    ax.set_facecolor('#ffffff')  # Fondo blanco
    plt.grid(axis='y', linestyle='--', linewidth=0.5, alpha=0.6)

    if not data:
        plt.text(0.5, 0.5, "No hay datos para graficar", ha='center', va='center', fontsize=16, color='#888')
        plt.axis('off')
    else:
        clientes = [fila[0] for fila in data]
        montos = [float(fila[1]) for fila in data]

        barras = plt.bar(clientes, montos, color='#3498db', edgecolor='#2980b9', linewidth=1)

        for bar in barras:
            bar.set_linewidth(0.5)
            bar.set_edgecolor('#2c3e50')

        # Etiquetas de monto encima de cada barra
        for i, bar in enumerate(barras):
            plt.text(bar.get_x() + bar.get_width() / 2,
                     bar.get_height() + 0.5,
                     f"${montos[i]:,.2f}",
                     ha='center', va='bottom', fontsize=10, color='#2c3e50')

        plt.title("Créditos Otorgados por Cliente", fontsize=14, color='#2c3e50')
        plt.xlabel("Cliente", fontsize=12)
        plt.ylabel("Monto del Crédito", fontsize=12)
        plt.xticks(rotation=30)
        plt.tight_layout()

        # Bordes redondeados
        for bar in barras:
            bar.set_linewidth(0.5)
            bar.set_edgecolor('#2c3e50')

        plt.title("Créditos Otorgados por Cliente", fontsize=14, color='#2c3e50')
        plt.xlabel("Cliente", fontsize=12)
        plt.ylabel("Monto del Crédito", fontsize=12)
        plt.xticks(rotation=30)
        plt.tight_layout()

    output_path = os.path.join("static", "grafica.png")
    plt.savefig(output_path, bbox_inches='tight', dpi=100)
    plt.close()

    return send_file(output_path, mimetype="image/png")
