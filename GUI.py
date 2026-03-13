import customtkinter as ctk
'''
добавить textholder, поддержка файлов word txt, второй лейбл с результатом, мб иконку в таскбаре поменять 
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

        self.button = ctk.CTkButton(master=self,
                                    text="Проверить",
                                    command = self.check_btn_func,
                                    width=312, height=81,
                                    corner_radius=10,
                                    fg_color="#53B962",
                                    hover_color="#59CF6A")
        self.check_entry = ctk.CTkTextbox(master=self,
                                        wrap = "word",
                                        width=312,
                                        height=394,
                                        )

        self.check_entry.place(x=16, y=50)


        self.button.place(x= 16, y=482)

    def check_btn_func(self):
        checktext = self.check_entry.get("1.0", "end").strip()
        if len(checktext) > 0:
            print(checktext)
            #будет поменяно на функцию каку-то
        else:
            print("Введите что-нибудь")
            #потом будет на лэйбле втором где результат

if __name__ == '__main__':
    app = App()
    app.mainloop()