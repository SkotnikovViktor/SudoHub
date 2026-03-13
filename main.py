import socket
import torch
from transformers import AutoTokenizer, AutoModelForMaskedLM
import math

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
            model_name = 'cointegrated/rubert-tiny2'

            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForMaskedLM.from_pretrained(model_name)
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
    



if __name__ == "__main__":
      
    # Пробный текст, сгенерированный ИИ
    test_text = """В далеком-далеком прошлом, когда папоротники были выше современных деревьев, жил маленький динозаврик по имени Крош. Он был не страшным хищником с острыми клыками, а милым травоядным ящером с мягкой зеленой чешуей и смешными пятнышками на хвосте.
Крош очень любил исследовать мир. Каждое утро он выбегал из уютной пещеры, щурился от яркого солнца и глубоко вдыхал воздух. Сегодня лес пах сладкими ягодами и влажной землей после дождя.
— Я буду самым храбрым! — сказал сам себе Крош и громко рыкнул. Но вместо грозного рева получилось тихое: «Пых-пых!».
Он не расстроился. Вместо того чтобы пугать других, Крош решил найти что-нибудь интересное. Он заглянул под большой лист и увидел светлячка, который потерял свой свет. Маленький динозаврик аккуратно подтолкнул жучка к цветку, где всегда горели теплые огоньки.
Вечером, когда луна осветила джунгли, Крош вернулся к маме. Он был уставший, но счастливый. Мама обняла его своим длинным хвостом и спросила:
— Что ты сегодня сделал важного?
— Я помог другу, — прошептал Крош и уснул.
Он понял, что быть маленьким динозавриком — это здорово. Можно прятаться в высокой траве, видеть мир снизу вверх и находить чудеса там, где большие динозавры просто проходят мимо."""

    a = CalPerplexity(test_text,"yandex.ru")
    print(a.result)