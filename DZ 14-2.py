#Задача "Средний баланс пользователя":
import sqlite3

conn = sqlite3.connect('not_telegram.db')
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        age INTEGER,
        balance INTEGER NOT NULL
    )
""")

users = [
    ('User1', 'example1@gmail.com', 10, 1000),
    ('User2', 'example2@gmail.com', 20, 1000),
    ('User3', 'example3@gmail.com', 30, 1000),
    ('User4', 'example4@gmail.com', 40, 1000),
    ('User5', 'example5@gmail.com', 50, 1000),
    ('User6', 'example6@gmail.com', 60, 1000),
    ('User7', 'example7@gmail.com', 70, 1000),
    ('User8', 'example8@gmail.com', 80, 1000),
    ('User9', 'example9@gmail.com', 90, 1000),
    ('User10', 'example10@gmail.com', 100, 1000)
]

cursor.executemany('INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)', users)
conn.commit()

cursor.execute('UPDATE Users SET balance = 500 WHERE id % 2 = 1')
conn.commit()

cursor.execute('DELETE FROM Users WHERE id % 3 = 1')
conn.commit()

cursor.execute('DELETE FROM Users WHERE id = 6')
conn.commit()

cursor.execute('SELECT username, email, age, balance FROM Users WHERE age != 60')
records = cursor.fetchall()

for record in records:
    username, email, age, balance = record
    print(f'Имя: {username} | Почта: {email} | Возраст: {age} | Баланс: {balance}')

cursor.execute('SELECT COUNT(*) FROM Users')
total_users = cursor.fetchone()  
print(f'Общее количество пользователей: {total_users}')

cursor.execute('SELECT SUM(balance) FROM Users')
all_balances = cursor.fetchone()  
print(f'Сумма всех балансов: {all_balances}')

if total_users > 0:
    average_balance = all_balances / total_users
    print(f'Средний баланс всех пользователей: {average_balance}')
else:
    print('Нет записей для расчета среднего баланса.')

conn.close()


Вывод:
Имя: User2 | Почта: example2@gmail.com | Возраст: 20 | Баланс: 1000
Имя: User3 | Почта: example3@gmail.com | Возраст: 30 | Баланс: 500
Имя: User5 | Почта: example5@gmail.com | Возраст: 50 | Баланс: 500
Имя: User8 | Почта: example8@gmail.com | Возраст: 80 | Баланс: 1000
Имя: User9 | Почта: example9@gmail.com | Возраст: 90 | Баланс: 500
Общее количество пользователей: (5,)
Сумма всех балансов: (3500,)
