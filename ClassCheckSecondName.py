import re
import wikipedia
import asyncio

class CheckSecondName:

    NAME_PATTERN= re.compile(r'(?<![А-ЯЁа-яё])(?:[А-ЯЁ][а-яё]+(?:-[А-ЯЁ][а-яё]+)?|[А-ЯЁ]\.)(?:\s+(?:[А-ЯЁ][а-яё]+(?:-[А-ЯЁ][а-яё]+)?|[А-ЯЁ]\.)){0,2}(?![А-ЯЁа-яё])', flags = re.VERBOSE) # Создание паттерна 

    

    def __init__(self, text: str):
        self.text = text
        self.list_second_name = re.findall(self.NAME_PATTERN, self.text)
        self.result_procent = 0
        self.result = {"procent": ..., "veriefy_name": ..., "not_variefy_name": ...}
        self.count_verify_name = 0

        self.list_verify_name = []
        self.list_not_verify_name = []

        asyncio.run(self.__check_name_in_wiki())
    



    async def __check_name_in_wiki(self):

        for name in self.list_second_name:
            result_checking = wikipedia.search(name.strip())

            if len(result_checking) != 0:
                self.count_verify_name += 1
                self.list_verify_name.append(name)
            
            else:
                self.list_not_verify_name.append(name)
            


        try: # Проверка переменной известных имён на не 0
            self.result_procent = (self.count_verify_name * 100) / len(self.list_second_name) 
        except ZeroDivisionError: # Если переменная 0, то без подсчёта присваевыем 0
            self.result_procent = 0 
        

        # Формирования словаря с данными: процент, массив известных имён, массив неизвестных имён
        self.result["procent"] = self.result_procent
        self.result["veriefy_name"] = self.list_verify_name
        self.result["not_variefy_name"] = self.list_not_verify_name
    
    

    # Геттер, который возвращает словрь данных
    def getter(self):
        return self.result



