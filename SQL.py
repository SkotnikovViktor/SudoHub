import sqlite3

# Подключение к DataBase
conn = sqlite3.connect('Data\Main.db')
cursor = conn.cursor()

# Удаление прошлой таблицы
cursor.execute("DROP IF EXIST TABLE Work")

# Создание талицы
cursor.execute("CREATE TABLE IF NOT EXISTS Work (word TEXT NOT NULL, count INT);")

# Чтение данных
cursor.execute("INSERT INTO Work (word) SELECT * FROM Words;")
cursor.execute("SELECT word FROM Work")

words = cursor.fetchall()

for i in range(len(words)):
    
    word = words[i][0]

    count = vasily_program(word)

    cursor.execute(f"UPDATE Work SET count = {count} WHERE word = {word};")

# Что сделать с количеством надо?

# Сохранение данных и закрытие соединения
conn.commit()
conn.close()
