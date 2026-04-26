import requests
import re
import asyncio


class ClassDetectedWhiteList: # Класс для првоерки белых списков

    def __init__(self):
        self.list_check_website = ["https://www.deepseek.com/en/", "https://github.com"]
        self.result = 0 # Переменная результата
        self.__detected_white_list()



    def __detected_white_list(self) -> int:
        

        for website in range(2):

            try: 
                requests.head(self.list_check_website[website]) # Отправляем HEAD запрос 
            except Exception as e:
                self.result += 1



            try:
                requests.get(self.list_check_website[website], timeout = 3) # Отправляем GET запрос
            except Exception as e:
                self.result += 1
            


        if self.result is None:
            self.result = 0

        elif 2 <= self.result <= 4: 
            self.result = 1
        
        else:
            self.result = 0
    



    def getter(self) -> int:
        return self.result






class ClassCheckingLink:

    URL_PATTERN = re.compile(r'''(?xi)
    \b(?:https?://|www\.)
    [^\s<>"{}|\\^`\[\]]+
    (?<![.,;:!?])
    ''', flags=re.VERBOSE) # Создание паттерна для поиска ссылок

    def __init__(self, text: str, timeout) -> None:
        self.text = text
        self.result = None
        self.timeout = timeout
        self.list_link = re.findall(self.URL_PATTERN, self.text)
        self.count_work_link = 0
        asyncio.run(self.__function_count_procent_work_link())
        
      


    async def __function_check_link(self, url: str) -> bool | Exception:

        detected_white_list = ClassDetectedWhiteList() # Проверка на белые списки
        if detected_white_list.getter() == 1:
            return "WhiteList"


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


        

        if self.list_link is None and self.count_work_link != 0 and self.list_link != "В тексте нет ссылок":
            self.result = (self.count_work_link * 100) / len(self.list_link) 
        
        elif self.count_work_link == 0:
            self.result = 0

        elif self.result == "В тексте нет ссылок":
            self.result = "В тексте нет ссылок"
    


    def getter(self):
        print(self.result)
        return self.result # Геттер возвращает результат количество рабочих ссылок
    



    





