import socket
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import math
import re
import requests




class CalPerplexity:
    def __init__(self, text: str, host: str):
        self.text = text
        self.host = host
        self.tokenizer = None
        self.model = None
        self.result = None



        # Проверка подключения к интернету для скачивания моделей
        status_connect = self.is_connect(self.host) 
        if status_connect == False:
            print("[WARNING] Отсутствует подключение к интернету, загрузка моделей игнорируется.")
            return
        
        else:
            print("[INFO] Загрузка модели...")
            # Начинаем загрузку моделей в отдельном потоке демоне программы 
            if self.downloads_model() and self.tokenizer != None:
                self.text_verification(self.text)
        



    def is_connect(self, host: str) -> bool:
        try:
            with socket.create_connection((host, 80), timeout=2):
                return True
        
        except OSError:
            return False
            

    


    def downloads_model(self):
        try:
            model_name = 'ai-forever/rugpt3small_based_on_gpt2' # Разобраться, скачав на пк

            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForCausalLM.from_pretrained(model_name)
            self.model.eval()
            print("[INFO] Модель успешно загружена")
            return True
        

        except:
            print("[ERROR] Ошибка скачивания модели")
            return False




    def text_verification(self, text):
        inputs = self.tokenizer(text, return_tensors='pt', truncation=True, max_length=512)
        with torch.no_grad():
            outputs = self.model(**inputs, labels=inputs['input_ids'])
            loss = outputs.loss
        self.result = math.exp(loss.item())






class CheckingForOriginality:
    def __init__(self, text: str):
        self.text = text
        self.link = 0
        self.result = None


        self.pattern = r'''(?xi)
                    \b(?:
                    https?://|
                    www\.
                            )
                    [^\s<>"{}|\\^`\[\]]+
                    (?<![.,;:!?])
                    '''

        """При возвращении списка подходящих элементов считаем количество"""
        list_links = re.findall(self.pattern, self.text)


        for link in list_links:
            if self.ping_link(link.strip()):
                self.link += 1
        
        if len(list_links) != 0 and self.link != 0:
            self.result = (self.link * 100) / len(list_links)
        
        else:
            return
        
        
    



    def ping_link(self, link: str):

        
        try:
            ping = requests.get(link, timeout = 2)
            if 200 <= ping.status_code <= 300:
                return True
            return False
    
        except:
            return False

        







if __name__ == "__main__":
      
    # Пробный текст, набранный рандомно вручную PPL~557
    test_text = """рарарвтт тарпрпо опрповлвл рпрпоала рпрармтмт  привет как дела псяса кук опара"""

    a = CalPerplexity(test_text,"yandex.ru")
    print(a.result)


    b = CheckingForOriginality(test_text)
    if b.result == None:
        print("[WARNING]В тексте отсутствуют ссылки")
    
    else:
        print(f"Процент рабочих ссылок: {b.result}")