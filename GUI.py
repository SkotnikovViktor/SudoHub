import customtkinter as ctk
from PIL import Image as IMG

'''
поддержка файлов word txt DRAG N DROP 
'''
class App(ctk.CTk):
    def __init__(self):
        ctk.CTk.__init__(self)
        self.configure(fg_color='#3E304D')# фон окна
        self.geometry("703x619") #размер окна
        self.title("SudoHub") # название окна
        self.resizable(False, False) # зиприт на измэнения

        #ебля с иконкой
        icopath = "Assets/Images/ICO.ico"
        self.iconbitmap(icopath)

        #кнопка
        self.button = ctk.CTkButton(master=self,
                                    text="Проверить",
                                    command = self.check_btn_func,
                                    width=312,
                                    height=81,
                                    corner_radius=10,
                                    fg_color="#53B962",
                                    hover_color="#59CF6A")
        #то куда надо вводить
        self.check_entry = ctk.CTkTextbox(master=self,
                                        wrap = "word",
                                        width=312,
                                        height=394,
                                        )
        #текст просто
        self.resultLabel = ctk.CTkLabel(master=self,
                                        height=28,
                                        width=313,
                                        bg_color="#E7F3EF",
                                        text="Результат проверки",
                                        )
        #результат проверки
        self.resultLabel2 = ctk.CTkTextbox(master=self,
                                         height=480,
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


        '''картинка файлов'''
        fileimage = IMG.open("Assets/Images/file.png")
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
        self.resultLabel2.place(x=358, y=80)


        #рамка
        sepatator = ctk.CTkFrame(master=self, height=2, fg_color="black", width=313)
        sepatator.place(x=358, y=50+28)

    def check_btn_func(self):
        self.resultLabel2.configure(state="normal")
        self.resultLabel2.delete("1.0", "end")
        self.resultLabel2.configure(state="disabled")
        checktext = self.check_entry.get("1.0", "end").strip()
        if len(checktext) > 0 and checktext != self.textholder:
            self.resultLabel2.configure(state="normal")
            self.resultLabel2.insert("1.0", checktext) #поменять на функцию
            self.resultLabel2.configure(state="disabled")
        else:
            self.resultLabel2.configure(state="normal")
            self.resultLabel2.insert("1.0", "Введите что-нибудь")
            self.resultLabel2.configure(state="disabled")

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



if __name__ == '__main__':
    app = App()
    app.mainloop()