import os
import sys
import random
import string
import json
import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk


def generate_password(length, include_digits=True, include_symbols=True):
    characters = string.ascii_letters + (string.digits if include_digits else '') + (
        string.punctuation if include_symbols else '')
    return ''.join(random.choice(characters) for _ in range(length))


def save_to_file(data, filename, translations):
    with open(filename, "a") as file:
        for website, info in data.items():
            file.write(f"Website: {website}, Username/Email: {info['username']}, Password: {info['password']}\n")
    messagebox.showinfo(translations["Success"], translations["Data saved to"] + f" {filename}")


class PasswordGeneratorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.iconphoto(False, tk.PhotoImage(file=self.resource_path('brain.png')))
        self.translations = {}
        self.current_language = 'english'
        self.load_translations(self.current_language)
        self.title(self.translations["Password Generator App"])
        self.geometry("400x440")
        self.setup_ui()

    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def load_translations(self, language):
        with open(self.resource_path(f"translations/{language}.json"), "r", encoding='utf-8') as file:
            self.translations = json.load(file)

    def setup_ui(self):
        for widget in self.winfo_children():
            widget.destroy()

        title_frame = tk.Frame(self)
        title_frame.pack(pady=10)

        title_label = tk.Label(title_frame, text=self.translations["Password Generator App"], font=("Arial", 14))
        title_label.pack()


        image_path = self.resource_path('brain.png')
        app_image = Image.open(image_path)
        resized_image = app_image.resize((50, 50), Image.Resampling.LANCZOS) 
        self.app_photo_image = ImageTk.PhotoImage(resized_image)
        image_label = tk.Label(self, image=self.app_photo_image)
        image_label.pack(pady=10)

        form_frame = tk.Frame(self)
        form_frame.pack(pady=10)

        tk.Label(form_frame, text=self.translations["Website"]).grid(row=0, column=0, sticky="w")
        self.website_entry = tk.Entry(form_frame, width=20)
        self.website_entry.grid(row=0, column=1)

        tk.Label(form_frame, text=self.translations["Username/Email"]).grid(row=1, column=0, sticky="w")
        self.username_entry = tk.Entry(form_frame, width=20)
        self.username_entry.grid(row=1, column=1)

        tk.Label(form_frame, text=self.translations["Password Length"]).grid(row=2, column=0, sticky="w")
        self.length_entry = tk.Entry(form_frame, width=5)
        self.length_entry.insert(0, "12")
        self.length_entry.grid(row=2, column=1, sticky="w")

        self.include_digits_var = tk.BooleanVar(value=True)
        self.digits_checkbutton = tk.Checkbutton(form_frame, text=self.translations["Include Digits"],
                                                 variable=self.include_digits_var)
        self.digits_checkbutton.grid(row=3, column=0, sticky="w")

        self.include_symbols_var = tk.BooleanVar(value=True)
        self.symbols_checkbutton = tk.Checkbutton(form_frame, text=self.translations["Include Symbols"],
                                                  variable=self.include_symbols_var)
        self.symbols_checkbutton.grid(row=3, column=1, sticky="w")

        generate_button = tk.Button(form_frame, text=self.translations["Generate"], command=self.generate)
        generate_button.grid(row=4, column=0, columnspan=2, pady=5)

        result_frame = tk.Frame(self)
        result_frame.pack(pady=10)

        tk.Label(result_frame, text=self.translations["Generated Password"]).grid(row=0, column=0, sticky="w")
        self.generated_password_entry = tk.Entry(result_frame, width=20)
        self.generated_password_entry.grid(row=0, column=1, pady=5)

        save_button = tk.Button(result_frame, text=self.translations["Save to File"], command=self.save)
        save_button.grid(row=1, column=0, columnspan=2)

        language_frame = tk.Frame(self)
        language_frame.pack(pady=10)

        language_label = tk.Label(language_frame, text=self.translations["Select language"])
        language_label.pack()

        tk.Button(language_frame, text='EN', command=lambda: self.change_language('english')).pack(side=tk.LEFT)
        tk.Button(language_frame, text='RU', command=lambda: self.change_language('russian')).pack(side=tk.LEFT)
        tk.Button(language_frame, text='LT', command=lambda: self.change_language('lithuanian')).pack(side=tk.LEFT)

        copyright_frame = tk.Frame(self)
        copyright_frame.pack(side=tk.BOTTOM, fill=tk.X)
        copyright_label = tk.Label(copyright_frame, text="©2023", font=("Arial", 10))
        copyright_label.pack()

    def generate(self):
        try:
            length = int(self.length_entry.get())
            include_digits = self.include_digits_var.get()
            include_symbols = self.include_symbols_var.get()
            generated_password = generate_password(length, include_digits, include_symbols)
            self.generated_password_entry.delete(0, tk.END)
            self.generated_password_entry.insert(0, generated_password)
        except ValueError:
            messagebox.showerror(self.translations["Error"], self.translations["Please enter a valid length"])

    def save(self):
        website = self.website_entry.get()
        username = self.username_entry.get()
        password = self.generated_password_entry.get()
        if not all([website, username, password]):
            messagebox.showerror(self.translations["Error"], self.translations["Please generate a password first"])
            return
        data = {website: {'username': username, 'password': password}}
        filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if filename:
            save_to_file(data, filename, self.translations)

    def change_language(self, language):
        self.current_language = language
        self.load_translations(language)
        self.setup_ui()


if __name__ == "__main__":
    app = PasswordGeneratorApp()
    app.mainloop()