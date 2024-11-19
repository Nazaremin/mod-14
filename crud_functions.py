import sqlite3

def initiate_db():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Products (
            id INTEGER PRIMARY KEY UNIQUE,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            price REAL NOT NULL
        )
    ''')

    products = [
        (1, 'Гейнер', 'пищевая добавка при спортивном питании', 1600),
        (2, 'Протеин', 'пищевая добавка при спортивном питании', 1200)
    ]

    cursor.executemany('''
        INSERT INTO Products (id, title, description, price)
        VALUES (?, ?, ?, ?)
        ON CONFLICT (id) DO UPDATE SET
            title = excluded.title,
            description = excluded.description,
            price = excluded.price
    ''', products)

    conn.commit()
    conn.close()


initiate_db()

def get_all_products():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Products')
    products = cursor.fetchall()
    conn.close()
    return products
