import socket
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import math
from pathlib import Path
from typing import Optional
import GUI 




class CalPerplexity:
    MODEL_PATH = Path("Models/ai-forever/rugpt3small_based_on_gpt2") # Путь до локальной модели


    def __init__(self, text: str, host: str):
        self.text = text
        self.host = host
        self.tokenizer = None
        self.model = None
        self.result = None



        
        if not self.MODEL_PATH.exists():
            if self.is_connect(self.host) == False:
                print("[WARNING] Модель не будет загружена, локальная отсутствует.")
                return
        
            else:
                print("[INFO] Загрузка модели...")
                self.downloads_model()
                self.text_verification(self.text)
        else:
            print("[INFO] Используется локальная модель...")
        

            if self.downloads_local_model() and self.tokenizer != None:
                    self.text_verification(self.text)
        



    def is_connect(self, host: str) -> bool:
        try:
            with socket.create_connection((host, 80), timeout=2):
                return True
        
        except OSError:
            return False
            

    


    def downloads_model(self): # Функция для скачивания модели, если её нет
        try:
            model_name = 'ai-forever/rugpt3small_based_on_gpt2' 

            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForCausalLM.from_pretrained(model_name)

            self.MODEL_PATH.mkdir(parents = True, exist_ok = True)
            self.tokenizer.save_pretrained(self.MODEL_PATH)
            self.model.save_pretrained(self.MODEL_PATH)

            print("[INFO] Модель сохранена в {self.MODEL_PATH}")
            return True
        

        except Exception as e :
            print(f"[ERROR] Ошибка скачивания модели - {e}")
            return False
        

        



    def downloads_local_model(self):
        try:

            self.tokenizer = AutoTokenizer.from_pretrained(self.MODEL_PATH)
            self.model = AutoModelForCausalLM.from_pretrained(self.MODEL_PATH)
            self.model.eval()
            print("[INFO] Локальная модель загружена")
            return True
        
        except Exception as e:
            print(f"[ERROR] Ошибка загрузки локальной модели: {e}")
            return False






    def text_verification(self, text):
        inputs = self.tokenizer(text, return_tensors='pt', truncation=True, max_length=512)
        with torch.no_grad():
            outputs = self.model(**inputs, labels=inputs['input_ids'])
            loss = outputs.loss
        self.result = math.exp(loss.item())


if __name__ == "__main__":
      
    # Пробный текст, набранный рандомно вручную для проверки ссылок
    test_text = """https://chat.qwen.ai/c/61c002ef-5279-4873-a4dc-94114d565791 ропопропоп https://github.com/SkotnikovViktor/SudoHub/commit/5f10240a99c31bf3da00e804cf857dccc54939da аопопо https://githuy.com """

    a = CalPerplexity(test_text,"yandex.ru")
    print(a.result)


    result = asyncio.run(AsyncCheckingForOriginality.check(test_text, timeout=5, concurrency=30))

    if result == None:
        print("[INFO]В тексте отсутствуют ссылки")
    
    else:
        print(f"Процент рабочих ссылок: {round(result)} %")