import sqlite3

# Подключение к DataBase
conn = sqlite3.connect('Learning.db')
cursor = conn.cursor()

# Создание талицы
cursor.execute('''
CREATE TABLE Test_2 (
    id INT PRIMARY KEY,
    name TEXT NOT NULL,
    age INT
)
''')

# Вставка данных
cursor.execute("INSERT INTO Test_2 (id, name, age) VALUES (?, ?, ?)", (0, 'Михаил', 18))

# Чтение данных
cursor.execute("SELECT * FROM Test_2")

rows = cursor.fetchall()

for row in rows:
    print(row)

# Сохранение данных и закрытие соединения
conn.commit()
conn.close()