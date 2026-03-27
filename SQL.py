import sqlite3, alg_wrapper

def search (text):
    # Подключение к DataBase
    conn = sqlite3.connect('Data/Main.db')
    cursor = conn.cursor()
    
    # Удаление прошлой таблицы
    cursor.execute("DROP TABLE IF EXISTS Work")
    
    # Создание талицы
    cursor.execute("CREATE TABLE IF NOT EXISTS Work (word TEXT NOT NULL, count INT);")
    
    # Чтение данных
    cursor.execute("INSERT INTO Work (word) SELECT * FROM Words;")
    cursor.execute("SELECT word FROM Work")
    
    words = cursor.fetchall()
    
    for i in range(len(words)):
        
        word = words[i][0]
    
        count = alg_wrapper.knut_morris_pratta(word, text)
    
        cursor.execute(f"UPDATE Work SET count = {count} WHERE word = {word};")
    
    result = cursor.execute("SELECT * FROM Work")

    for i in range(len(result)):
        print(f"{i[0]}:{i[1]}")
    
    # Сохранение данных и закрытие соединения
    conn.commit()
    conn.close()
