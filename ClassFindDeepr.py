import pymorphy3
import re


class ClassFindDeepr:

    def __init__(self, text):

          

        base_symbol = r"!,.:;?\/-_"
        self.text = text

        for symbol in base_symbol: # Очистка текста от знаков
            self.text = self.text.replace(symbol, "")


        self.morph = pymorphy3.MorphAnalyzer()
        self.words = re.findall(r'\w+', text)
        self.result = {"count_deepr_in_text":..., "normal_for_person":"0.9>=", "normal_for_ai":"0.8<="}
        self.len_text = len(text)
        self.__detected_deepr()
    


    def __detected_deepr(self):

        count_deepr = 0

        for word in self.words:
            parse = self.morph.parse(word)[0]
            if 'GRND' in parse.tag:
                count_deepr += 1 # Считаем количество деепричастий
        
        if count_deepr != 0:
            self.result["count_deepr_in_text"] = (count_deepr / self.len_text) * 100
        
        elif count_deepr == 0:
            self.result["count_deepr_in_text"] = 0 # Если количество деепричастий ноль, то результат 0
    



    def getter(self):
        return self.result
    








        
