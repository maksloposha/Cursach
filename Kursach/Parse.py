from tkinter import messagebox
class Parse:
    def get_value(self, entry):
        value = entry.get()
        try:
            return value
        except ValueError:
            return None

    def convert_to_int(self, entry):
        value = self.get_value(entry)
        try:
            return int(value)
        except ValueError:
            messagebox.showinfo("Неправильний ввід", "Введіть число ще раз")
            return None

    def convert_to_str(self, entry, nodes):
        letter = self.get_value(entry)
        if letter == "":
            messagebox.showinfo("Неправильний ввід", "Ви не ввели вузол\nВведіть вузол")
            return
        if letter not in nodes :
            messagebox.showinfo("Неправильний ввід", "Не існує такого вузла\nВведіть вузол ще раз")
            return None
        else:
            return str(letter)
