import requests
import re
import asyncio

class ClassCheckingLink:

    URL_PATTERN = re.compile(r'''(?xi)
    \b(?:https?://|www\.)
    [^\s<>"{}|\\^`\[\]]+
    (?<![.,;:!?])
    ''', flags=re.VERBOSE) # Создание паттерна для поиска ссылок

    def __init__(self, text: str, timeout = 10) -> None:
        self.text = text
        self.result = None
        self.timeout = timeout
        self.list_link = re.findall(self.URL_PATTERN, self.text)
        self.count_work_link = 0
        asyncio.run(self.__function_count_procent_work_link())
        
      


    async def __function_check_link(self, url: str) -> bool | Exception:
        try:
            respone = requests.head(url = url, timeout = self.timeout, allow_redirects = True) # Отправляем HEAD запрос

            if respone.status_code == 405: # Если сайт блокирует HEAD запрос, отправляем GET
                respone = requests.get(url = url, timeout = self.timeout, allow_redirects = True) # Отправляем GET запрос

            
            if respone.status_code == 200 or 300 <= respone.status_code < 400:
                return True # Ссылка рабочая

            else:
                return False
            
        except requests.exceptions.RequestException as error_check_link:
            return error_check_link    




    async def __function_count_procent_work_link(self):

        if len(self.list_link) == 0:
            self.result = "В тексте нет ссылок"

        else:    
            for link in self.list_link:

                result = await self.__function_check_link(link)
                if  result == True:
                    self.count_work_link += 1
                
                elif isinstance(result, requests.exceptions.RequestException):
                    continue
        

        try: # Проверка переменной рабочих ссылок на не 0
            self.result = (self.count_work_link * 100) / len(self.list_link) 
        except ZeroDivisionError: # Если переменная 0, то без подсчёта присваевыем 0
            self.result = 0 
    


    def getter(self):
        return self.result # Геттер возвращает результат количество рабочих ссылок
    





#res = CheckingLink("https://lordserialzinc.lol/82-vstat-na-nogi-u62k.html fdjgf https://lordserialin.ol/82-vstat-na-nogi-u62k.html", 10)
#print(res.getter())


"""Как работать с классом? Во-первых нужно создать объект класса как в 77 строчке, название можно выбрать любое.
Во-вторых, из ранее созданого объекта нужно вызвать функцию getter() как в 78 строчке и сохранить в переменную результат проверки"""


    





