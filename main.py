import threading
import customtkinter as ctk




class Loader(ctk.CTk):
    def __init__(self):
        ctk.CTk.__init__(self)
        self.overrideredirect(True)
        self.configure(fg_color='#4A4563')  # фон окна
        width = 400
        height = 200
        user_height = self.winfo_screenheight()
        user_width = self.winfo_screenwidth()
        self.geometry(f"{width}x{height}+{(user_width-width) // 2}+{(user_height-height) // 2}")
        

        self._set_appearance_mode("light")

        ctk.CTkLabel(self,
                     text="SudoHub",
                     font=("Arial", 36, "bold"),
                     text_color="white",).pack(pady=30)
        self.status_bar = ctk.CTkLabel(self,
                                       text="Запуск",
                                       font=("Arial", 12,),
                                       text_color="white",)
        self.status_bar.pack()
        self.progress_bar = ctk.CTkProgressBar(self, width=320,
                                               height=20,
                                               progress_color="#59CF6A",
                                               )
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=20)

    def update_loaderUI(self, text, progress):
        self.progress_bar.set(progress/100)
        self.status_bar.configure(text=text)

    def set_status(self, text, progress):
        self.after(0, self.update_loaderUI, text, progress)

    def start(self):
        threading.Thread(target=self.load, daemon=True).start()
        self.mainloop()

    def load(self):
        self.set_status("Загрузка PIL...", 10)
        from PIL import Image

        self.set_status("Загрузка DND...", 20)
        from tkinterdnd2 import DND_FILES, TkinterDnD

        self.set_status("Загрузка PDF, DOCX", 30)
        import fitz  # pdf
        import docx  # word

        self.set_status("Загрузка графики...", 40)
        from tkinter import messagebox
        from tkinter import filedialog

        self.set_status("Загрузка модели...", 50)
        from ClassPerplexity import CalPerplexity
        CalPerplexity("1", "yandex.ru", "-m") 

        self.set_status("Загрузка анализатора ссылок", 60)
        from CheckingLink import ClassCheckingLink

        self.set_status("Загрузка остального", 80)
        from Clib.ToolsForCompile.main import resultSpacesAndCount
        from ClassFindDeepr import ClassFindDeepr

        self.set_status("Готово, запускаю приложение", 100)
        self.after(0, self.openGui)

    def openGui(self):
        self.destroy()
        from GUI import App
        app = App()
        app.mainloop()


if __name__ == "__main__":
    Loader().start()