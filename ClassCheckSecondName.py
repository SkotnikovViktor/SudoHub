import re
import wikipedia
import asyncio

class CheckSecondName:

    NAME_PATTERN= re.compile(r'(?<![А-ЯЁа-яё])(?:[А-ЯЁ][а-яё]+(?:-[А-ЯЁ][а-яё]+)?|[А-ЯЁ]\.)(?:\s+(?:[А-ЯЁ][а-яё]+(?:-[А-ЯЁ][а-яё]+)?|[А-ЯЁ]\.)){0,2}(?![А-ЯЁа-яё])', flags = re.VERBOSE) # Создание паттерна 

    

    def __init__(self, text: str):
        self.text = text
        self.list_second_name = re.findall(self.NAME_PATTERN, self.text)
        print(self.text ,self.list_second_name)
        self.result = None
        self.count_verify_name = 0
        asyncio.run(self.__check_name_in_wiki())
    



    async def __check_name_in_wiki(self):

        for name in self.list_second_name:
            result_checking = wikipedia.search(name.strip())

            if len(result_checking) != 0:
                self.count_verify_name += 1
            


        try: # Проверка переменной известных имён на не 0
            self.result = (self.count_verify_name * 100) / len(self.list_second_name) 
        except ZeroDivisionError: # Если переменная 0, то без подсчёта присваевыем 0
            self.result = 0 
    
    


    def getter(self):
        return self.result




text = "Тестинг А. С. уппупупуп"
res = CheckSecondName(text)
print(res.getter())
