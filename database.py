import sqlite3

def create_db():
    conn = sqlite3.connect('creditos.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS creditos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente TEXT NOT NULL,
            monto REAL NOT NULL,
            tasa REAL NOT NULL,
            plazo INTEGER NOT NULL,
            fecha TEXT NOT NULL,
            notas TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Ejecutar esta función al iniciar el proyecto
if __name__ == "__main__":
    create_db()
