import re
import wikipedia
import asyncio
import time

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


full_names = """
Иванов Иван Иванович
Петрова Анна Сергеевна
Сидоров Петр Михайлович
Кузнецова Елена Викторовна
Смирнов Алексей Андреевич
Попова Ольга Дмитриевна
Васильев Дмитрий Алексеевич
Соколова Татьяна Николаевна
Михайлов Сергей Павлович
Новикова Екатерина Валерьевна
Федоров Андрей Васильевич
Морозова Наталья Игоревна
Волков Игорь Александрович
Алексеева Светлана Юрьевна
Лебедев Константин Олегович
Семенова Мария Антоновна
Егоров Владимир Степанович
Павлова Ирина Владимировна
Козлов Артем Романович
Степанова Юлия Аркадьевна
Николаев Виктор Евгеньевич
Орлова Дарья Борисовна
Андреев Никита Ильич
Макарова Анастасия Павловна
Никитин Глеб Витальевич
Захарова Ксения Львовна
Зайцев Матвей Данилович
Соловьева Валерия Максимовна
Борисов Арсений Кириллович
Яковлева Полина Егоровна
Григорьев Тимофей Федорович
Романова Варвара Семеновна
Воробьев Даниил Миронович
Фролова Алиса Георгиевна
Медведев Лев Ярославович
Белова Ева Тимуровна
Тарасов Марк Вячеславович
Комарова София Артемовна
Киселев Платон Денисович
Калинина Милана Эмильевна
Гусев Филипп Богданович
Фомина Александра Леонидовна
Быков Давид Робертович
Осипова Вера Геннадьевна
Герасимов Борис Эдуардович
Титова Диана Артуровна
Ковалев Леонид Викторович
Казакова Эмилия Марковна
Ефимов Святослав Натанович
Виноградова Ясмина Станиславовна
Антонов Максим Петрович

"""

start = time.time()
result = CheckSecondName(full_names)
end = time.time()


print(result.getter(), end - start)

