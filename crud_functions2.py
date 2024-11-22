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

    # Create the Users table if it does not exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            age INTEGER NOT NULL,
            balance INTEGER NOT NULL DEFAULT 1000
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

def add_user(username, email, age):
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT INTO Users (username, email, age)
            VALUES (?, ?, ?)
        ''', (username, email, age))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"User with username '{username}' or email '{email}' already exists.")
    finally:
        conn.close()

def is_included(username):
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT 1 FROM Users WHERE username = ?
    ''', (username,))

    result = cursor.fetchone()
    conn.close()

    return result is not None

def get_all_products():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Products')
    products = cursor.fetchall()
    conn.close()
    return products
