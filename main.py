#ПОЧЕМУ В MAIN???
import socket
import torch
from transformers import AutoTokenizer, AutoModelForMaskedLM
import threading
import math

class CalPerplexity:
    def __init__(self, text: str, host: str):
        self.text = text
        self.host = host

        # Проверка подключения к интернету для скачивания моделей
        status_connect = self.is_connect(self.host) 
        if status_connect == False:
            print("[WARNING] Отсутствует подключение к интернету, загрузка моделей игнорируется.")
            return -1
        
        else:
            print("[INFO] Загрузка модели")
            # Начинаем загрузку моделей в отдельном потоке демоне программы 
            load = threading.Thread(self.downloads_model, deamon = True) 
            load.start()




    def is_connect(self, host: str) -> bool:
        try:
            with socket.create_connection((host, 80), timeout=2):
                return True
        
        except OSError:
            return False
            

    

    def downloads_model(self):
        try:
            model_name = 'cointegrated/rubert-tiny2'

            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModelForMaskedLM.from_pretrained(model_name)
            model.eval()
            print("[INFO] Модель успешно загружена")
        
        except:
            print("[ERROR] Ошибка скачивания модели")



        def text_verification(text):
            inputs = tokenizer(text, return_tensors='pt', truncation=True, max_length=512)
            with torch.no_grad():
                outputs = model(**inputs, labels=inputs['input_ids'])
                loss = outputs.loss
            return math.exp(loss.item())
    
        text_verification(self.text)
        







  
CalPerplexity("fjf","yandex.ru")