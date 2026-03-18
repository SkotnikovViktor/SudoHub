import sqlite3

# Подключение к DataBase
conn = sqlite3.connect('Main.db')
cursor = conn.cursor()

# Создание талицы
cursor.execute("CREATE TABLE Work (id INT PRIMARY KEY AUTOINCREMENT, word TEXT NOT NULL, count INT)")

# Чтение данных
cursor.execute("INSERT INTO Work (word, count) SELECT * FROM Words ORDER BY count DESC;")
cursor.execute("SELECT COUNT(*) FROM Work")

for i in range(cursor.fetchall()):
    cursor.execute(f"SELECT word FROM Work WHERE id = {i+1};")
    inf = cursor.fetchall()

    Что-то делается

cursor.execute("DROP TABLE Work")

# Сохранение данных и закрытие соединения
conn.commit()
conn.close()
