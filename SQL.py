import sqlite3
import Clib.ToolsForCompile.main
import os
def search (text):
    # Создание словаря для возращения результата
    result = {}
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, 'Data', 'Main.db')
    # Подключение к DataBase
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Удаление прошлых данных
    cursor.execute("UPDATE Words SET count = 0")
    
    # Чтение данных
    cursor.execute("SELECT word FROM Words")
    
    words = cursor.fetchall()
    
    for i in range(len(words)):
        
        word = words[i][0]
    
        count = Clib.ToolsForCompile.main.knut_morris_pratta(word, text)
    
        cursor.execute(f"UPDATE Words SET count = {count} WHERE word = {word};")

        result[word] = count
    
    # Сохранение данных и закрытие соединения
    conn.commit()
    conn.close()

    # Возвращаем результат
    return result
