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
cursor.execute("CREATE TABLE Work AS SELECT * FROM Words")

# Сохранение данных и закрытие соединения
conn.commit()
conn.close()
