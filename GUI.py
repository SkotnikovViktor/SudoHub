import threading
import time
import customtkinter as ctk
import os
from PIL import Image
from tkinterdnd2 import DND_FILES, TkinterDnD
import fitz # pdf
import docx # word
import sys
from tkinter import messagebox
from tkinter import filedialog

# Локальные классы
from ClassPerplexity import CalPerplexity
from CheckingLink import ClassCheckingLink
from Clib.ToolsForCompile.main import resultSpacesAndCount
#from ClassCheckSecondName import CheckSecondName



class App(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self):
        ctk.CTk.__init__(self)
        self.TkdndVersion = TkinterDnD._require(self) # это типа регистрация чтобы self. и там были функции drop
        self.configure(fg_color='#4A4563')# фон окна
        self.geometry("703x619") #размер окна
        self.title("SudoHub") # название окна
        self.resizable(False, False) # зиприт на измэнения
        ctk.set_appearance_mode("light")
        self.isloading = False
        #Использяем try except для того чтобы точно установить иконку приложению независимо от ОС
        try:
            self.iconbitmap(self.resource_path("Assets/Images/ICO.ico"))
        except:
            self.iconbitmap(self.resource_path(r"Assets\Images\ICO.ico"))


        #кнопка
        self.button = ctk.CTkButton(master=self,
                                    text="Проверить",
                                    command = self.check_btn_func,
                                    width=312,
                                    height=81,
                                    corner_radius=10,
                                    fg_color="#59CF6A",
                                    hover_color="#7ade68",
                                    font = ("Arial", 30),
                                    text_color_disabled="#ffffff",)
        #кнопка сохранить
        self.buttonsave = ctk.CTkButton(master=self,
                                        text="Сохранить результат\n в текстовый файл",
                                        command= self.btn_save,
                                        width=312,
                                        height=81,
                                        corner_radius=10,
                                        fg_color="#9b46b8",
                                        hover_color="#ba58db",
                                        font=("Arial", 20),
                                        state="disabled",
                                        )
        #то куда надо вводить
        self.check_entry = ctk.CTkTextbox(master=self,
                                        bg_color="#ffffff",
                                        wrap = "word",
                                        width=312,
                                        height=422,
                                        )
        #текст просто
        self.resultLabel = ctk.CTkLabel(master=self,
                                        height=28,
                                        width=313,
                                        bg_color="#ffffff",
                                        text="Результат проверки",
                                        )
        #результат проверки
        self.resultEntryText = ctk.CTkTextbox(master=self,
                                              #height=480,
                                              height=394,
                                              width=313,
                                              bg_color="#E7F3EF",
                                              wrap="word",
                                              state="disabled",
                                              )
        #Добавление тегов
        self.resultEntryText._textbox.tag_configure("header", font=("Arial", 15, "bold"))
        self.resultEntryText._textbox.tag_configure("normal", font=("Arial", 13))

        #авторы
        self.authorsText = ctk.CTkLabel(master=self,
                                        text="Vladislav, Victor, Wasiliy, Michael",
                                        fg_color="#4A4563",
                                        font=("Arial", 16, "normal")
                                        )
        '''Текст холдер(жесть)'''
        self.textholder = "Введите текст для проверки\nили перетащите файл сюда"
        self.check_entry.bind("<FocusIn>", self.deleteplaceholder)
        self.check_entry.bind("<FocusOut>", self.writeplaceholder)
        self.check_entry.insert("1.0", self.textholder)
        self.check_entry.configure(text_color="grey")

        '''Drop files пиздец'''
        self.check_entry.drop_target_register(DND_FILES) # регистрация что я сюда могу кинуть файлы
        self.check_entry.dnd_bind("<<Drop>>", self.drop_inside_textBox) # действие на событие <<drop>>


        '''картинка файлов'''
        fileimage = Image.open(self.resource_path("Assets/Images/file.png"))
        self.icon_label = ctk.CTkImage(light_image=fileimage, dark_image=fileimage, size=(16, 16))
        self.label_fileimage = ctk.CTkLabel(master=self,
                                            image=self.icon_label,
                                            text='',
                                            width=16,
                                            height=16,
                                            bg_color='white',)

        '''размещения'''
        self.label_fileimage.place(x=197, y=73)
        self.check_entry.place(x=16, y=50)
        self.resultLabel.place(x=358, y=50)
        self.button.place(x= 16, y=482)
        self.resultEntryText.place(x=358, y=80)
        self.buttonsave.place(x= 358, y=482)
        self.authorsText.place(x=240, y=580)

        #рамка
        sepatator = ctk.CTkFrame(master=self, height=2, fg_color="black", width=313)
        sepatator.place(x=358, y=50+28)

    def check_btn_func(self):
        self.resultEntryText.configure(state="normal")
        self.resultEntryText.delete("1.0", "end")
        self.resultEntryText.configure(state="disabled")
        self.checktext = self.check_entry.get("1.0", "end").strip()
        if len(self.checktext) > 0 and self.checktext != self.textholder:
            self.isloading = True
            self.button.configure(state="disabled", fg_color="#59CF6A")
            self.buttonsave.configure(state="disabled")
            #loadingThread = threading.Thread(target=self.loadingBtn, daemon=True, args=(self, 0))
            #loadingThread.start()

            thread = threading.Thread(target=self.loadFunctions, daemon=True)
            thread.start()
            self.loadingBtn(0)

        else:
            self.resultEntryText.configure(state="normal")
            self.resultEntryText.insert("1.0", "Введите что-нибудь")
            self.resultEntryText.configure(state="disabled")

    def loadingBtn(self, step):
        texts = ["Загрузка...", "Загрузка..", "Загрузка."]
        if self.isloading == True:
            self.button.configure(text=texts[step%3])
            self.after(500, self.loadingBtn, step+1)


    def loadFunctions(self):
        self.Functions(self.checktext)
        self.after(200, self.FunctionsComplite) #Передать в лавный поток
        #self.FunctionsComplite(result)

    def append_result(self, text, tag="normal"):
        self.after(500, self.append_result_ui, text, tag)

    def append_result_ui(self, text, tag = "normal"):
        self.resultEntryText.configure(state="normal")
        self.resultEntryText.insert("end", text, tag)
        self.resultEntryText.configure(state="disabled")

    def FunctionsComplite(self):
        self.isloading = False
        self.button.configure(text="Проверить", state="normal")
        self.buttonsave.configure(state="normal")

    def Functions(self, checktext):
        time.sleep(0.1)
        self.append_result("Ссылки:\n", "header")
        time.sleep(0.1)
        self.resultCheckingLink = ClassCheckingLink(checktext, 3).getter()
        time.sleep(0.1)
        self.append_result(f"Процент рабочих ссылок  {self.resultCheckingLink}")
        time.sleep(0.1)

        '''
        self.append_result("\n\nИмена:\n", "header")
        resultCheckSecondName = CheckSecondName(checktext).getter()
        self.append_result("Известных имен в тексте: ")
        self.resultProcentSecondName = resultCheckSecondName.get("procent")
        self.append_result(self.resultProcentSecondName)
        self.append_result("\nИзвестные имена:  ")
        self.append_result(str(resultCheckSecondName.get("veriefy_name")).replace('[', '').replace(']', '    ').replace("\n", ", "))
        self.append_result("\nНеизвестные имена или выдуманные:  ")
        self.append_result(str(resultCheckSecondName.get("not_variefy_name")).replace('[', '').replace(']', '    ').replace("\n", ", "))
        '''

        self.append_result("\n\nДеепричастия\n", "header")
        time.sleep(0.1)
        self.append_result("\nКоличество деепричастий в тексте:   ")
        time.sleep(0.1)
        self.append_result("\nНорма для человека - М, норма для ИИ - Р")
        time.sleep(0.1)

        self.append_result("\n\nПредложения:\n", "header")
        time.sleep(0.1)
        resultspacesandcount = resultSpacesAndCount(checktext)
        self.spaces = resultspacesandcount[0]
        self.append_result(f"Количество пробелов в тексте {self.spaces}")
        time.sleep(0.1)
        self.points = resultspacesandcount[1]
        self.append_result(f"\nКоличество точек в тексте: {self.points}")
        time.sleep(0.1)

        self.append_result("\n\nДругое:\n", "header")
        time.sleep(0.1)
        self.resultPerlexity = CalPerplexity(checktext, "yandex.ru", "-f").getter().get("perpl")
        self.append_result(f"Перплексность: {self.resultPerlexity}")
        time.sleep(0.1)

        self.append_result("\n\nРезультат: ", "header")
        time.sleep(0.1)
        #функция проверки ИИ
        self.append_result("%ИИ")
        time.sleep(0.1)



    def writeplaceholder(self, event=None):
        if self.check_entry.get("1.0", "end").strip() == "":
            self.check_entry.insert("1.0", self.textholder)
            self.check_entry.configure(text_color="grey")
            self.label_fileimage.place(x=197, y=73)

    def deleteplaceholder(self, event=None):
        if self.check_entry.get("1.0", "end").strip() == self.textholder:
            self.check_entry.delete("1.0", "end")
            self.check_entry.configure(text_color="black")
            self.label_fileimage.place_forget()


    def drop_inside_textBox(self, event):
        filepatch = event.data.replace("{}", '').replace("{", '').replace("}", '')
        extension = os.path.splitext(filepatch)[1]
        #print(extension)
        content = ''
        if extension == ".txt":
            file = open(filepatch, "r", encoding="utf-8")
            try:
                for line in file:
                    content += line
            except:
                content = "Кодировка .txt не UTF-8"
            file.close()
        elif extension == ".pdf":
            file = fitz.open(filepatch)
            for page in file:
                content += page.get_text()
            file.close()
        elif extension == ".docx":
            file = docx.Document(filepatch)
            for paragraph in file.paragraphs:
                content += paragraph.text

        else:
            content = "Поддерживаемые типы: docx, txt, pdf"

        self.check_entry.delete("1.0", "end") # убрать текстхолдер
        self.check_entry.configure(text_color="black") # текст черный
        self.label_fileimage.place_forget() # скрыть картинку файла
        self.check_entry.insert("1.0", content) # записать содержимое файла

    def btn_save(self):
        result = self.resultEntryText.get("1.0", "end")
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text File", ".txt")])
        if file_path:
            file = open(file_path, "w", encoding="utf-8")
            count = 0
            for ch in result:
                file.write(ch)
                count += 1
                if count >= 80 and ch == ' ':
                    file.write("\n")
                    count = 0
            messagebox.showinfo("Файл сохранен", "Директория файла " + os.path.abspath(file_path))
            file.close()

    def resource_path(self, relative_path): #Для компиляции
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath('.'), relative_path)


if __name__ == '__main__':
    app = App()
    app.mainloop()
