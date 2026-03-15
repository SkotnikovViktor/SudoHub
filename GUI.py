import customtkinter as ctk
import os
from PIL import Image
from tkinterdnd2 import DND_FILES, TkinterDnD
import fitz # pdf
import docx # word

class App(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self):
        ctk.CTk.__init__(self)
        self.TkdndVersion = TkinterDnD._require(self) # это типа регистрация чтобы self. и там были функции drop
        self.configure(fg_color='#3E304D')# фон окна
        self.geometry("703x619") #размер окна
        self.title("SudoHub") # название окна
        self.resizable(False, False) # зиприт на измэнения

        # Использяем try except для того чтобы точно установить иконку приложению независимо от ОС
        try:
            self.iconbitmap("Assets/Images/ICO.ico")
        except:
            self.iconbitmap(r"Assets\Images\ICO.ico")


        #кнопка
        self.button = ctk.CTkButton(master=self,
                                    text="Проверить",
                                    command = self.check_btn_func,
                                    width=312,
                                    height=81,
                                    corner_radius=10,
                                    fg_color="#59CF6A",
                                    hover_color="#7ade68",
                                    font = ("Arial", 30))
        #кнопка сохранить
        self.buttonsave = ctk.CTkButton(master=self,
                                        text="Сохранить результат\n в txt",
                                        command= self.btn_save,
                                        width=312,
                                        height=81,
                                        corner_radius=10,
                                        fg_color="#9b46b8",
                                        hover_color="#ba58db",
                                        font=("Arial", 20)
                                        )
        #то куда надо вводить
        self.check_entry = ctk.CTkTextbox(master=self,
                                        bg_color="#ffffff",
                                        wrap = "word",
                                        width=312,
                                        height=394,
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
        fileimage = Image.open("Assets/Images/file.png")
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

        #рамка
        sepatator = ctk.CTkFrame(master=self, height=2, fg_color="black", width=313)
        sepatator.place(x=358, y=50+28)

    def check_btn_func(self):
        self.resultEntryText.configure(state="normal")
        self.resultEntryText.delete("1.0", "end")
        self.resultEntryText.configure(state="disabled")
        checktext = self.check_entry.get("1.0", "end").strip()
        if len(checktext) > 0 and checktext != self.textholder:
            self.resultEntryText.configure(state="normal")
            self.resultEntryText.insert("1.0", checktext) #поменять на функцию
            self.resultEntryText.configure(state="disabled")
        else:
            self.resultEntryText.configure(state="normal")
            self.resultEntryText.insert("1.0", "Введите что-нибудь")
            self.resultEntryText.configure(state="disabled")

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
        file = open("result", "w", encoding="utf-8")
        count = 0
        for ch in result:
            file.write(ch)
            count += 1
            if count >= 80 and ch == ' ':
                file.write("\n")
                count = 0

        file.close()
if __name__ == '__main__':
    app = App()
    app.mainloop()
