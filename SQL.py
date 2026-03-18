import sqlite3

# Подключение к DataBase
conn = sqlite3.connect('Main.db')
cursor = conn.cursor()

# Создание талицы
cursor.execute('''
CREATE TABLE Words (
    word TEXT NOT NULL,
    count INT
)
''')

# Чтение данных
cursor.execute("SELECT * FROM Test_2")

rows = cursor.fetchall()

for row in rows:
    print(row)

# Сохранение данных и закрытие соединения
conn.commit()
conn.close()
