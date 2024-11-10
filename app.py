from flask import Flask
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Platos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Mesas (
            numero INTEGER PRIMARY KEY
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plato_id INTEGER,
            mesa_numero INTEGER,
            cantidad INTEGER NOT NULL,
            fecha TEXT NOT NULL,
            FOREIGN KEY (plato_id) REFERENCES Platos(id),
            FOREIGN KEY (mesa_numero) REFERENCES Mesas(numero)
        )
    ''')

    # Insertar datos solo si las tablas están vacías
    cursor.execute('SELECT COUNT(*) FROM Platos')
    if cursor.fetchone()[0] == 0:
        platos = [
            ('Pizza', 8.5),
            ('Pasta', 7.5),
            ('Ensalada', 5.0),
            ('Sopa', 4.0),
            ('Taco', 3.5)
        ]
        cursor.executemany('INSERT INTO Platos (nombre, precio) VALUES (?, ?)', platos)

    cursor.execute('SELECT COUNT(*) FROM Mesas')
    if cursor.fetchone()[0] == 0:
        mesas = [(1,), (2,), (3,), (4,), (5,)]
        cursor.executemany('INSERT INTO Mesas (numero) VALUES (?)', mesas)

    cursor.execute('SELECT COUNT(*) FROM Pedidos')
    if cursor.fetchone()[0] == 0:
        pedidos = [
            (1, 1, 2, '2024-11-09'),
            (2, 2, 1, '2024-11-09'),
            (3, 3, 1, '2024-11-09'),
            (4, 4, 3, '2024-11-09'),
            (5, 5, 4, '2024-11-09')
        ]
        cursor.executemany('INSERT INTO Pedidos (plato_id, mesa_numero, cantidad, fecha) VALUES (?, ?, ?, ?)', pedidos)

    conn.commit()
    conn.close()

@app.route('/')
def index():
    return "Base de datos inicializada con éxito."

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
