import sqlite3, alg_wrapper

def search (text):
    # Подключение к DataBase
    conn = sqlite3.connect('Data/Main.db')
    cursor = conn.cursor()
    
    # Удаление прошлых данных
    cursor.execute("UPDATE Words SET count = 0")
    
    # Чтение данных
    cursor.execute("SELECT word FROM Words")
    
    words = cursor.fetchall()
    
    for i in range(len(words)):
        
        word = words[i][0]
    
        count = alg_wrapper.knut_morris_pratta(word, text)
    
        cursor.execute(f"UPDATE Words SET count = {count} WHERE word = {word};")
    
    result = cursor.execute("SELECT * FROM Words")

    for i in range(len(result)):
        print(f"{i[0]}:{i[1]}")
    
    # Сохранение данных и закрытие соединения
    conn.commit()
    conn.close()
