from abc import ABC, abstractmethod
import datetime
import os.path
import pickle


# Абстрактний клас для предметів, які можна зберігати.
class Storable(ABC):

    @abstractmethod
    def get_info(self):
        pass

# Клас, який представляє одну нотатку.


class Note(Storable):

    # Конструктор класу, який приймає текст нотатки та список ключових слів.
    def __init__(self, text='', keywords=None):
        self.text = text  # Текст нотатки.
        self.keywords = keywords  # Список ключових слів.
        self.date = datetime.date.today()  # Дата створення нотатки.

    # Метод, який повертає рядкове представлення нотатки.
    def get_info(self):
        return (f"Text: {self.text}\n"
                f"Keywords: {', '.join(self.keywords)}\n"
                f"Date: {self.date}")

    def __str__(self):
        return f"Text: {self.text}\nKeywords: {', '.join(self.keywords)}\nDate: {self.date}"


class Notebook:

    # Конструктор класу, який ініціалізує порожній список нотаток.
    def __init__(self):
        self.notes = []  # Список нотаток.

    # Метод, який додає нову нотатку до нотатника.
    def add_note(self, text='', keywords=None):

        # Створюємо екземпляр класу Note з заданим текстом та ключовими словами.
        if keywords:

            note = Note(text, keywords)
            self.notes.append(note)  # Додаємо запис до списку.

        else:

            # Створюємо екземпляр класу Note з заданим текстом без ключових слів.
            note = Note(text, keywords=[])
            self.notes.append(note)

    # Метод, який редагує існуючу нотатку за її індексом у списку.
    def edit_note(self, index, text=None, keywords=None):

        # Перевіряємо, чи є такий індекс у списку нотаток.
        if 0 <= index < len(self.notes):

            if text:  # Якщо заданий новий текст, то змінюємо текст нотатки.
                self.notes[index].text = text

            if keywords:  # Якщо заданий новий список ключових слів, то змінюємо ключові слова нотатки.
                self.notes[index].keywords = keywords

        else:
            # Якщо такого індексу немає, то виводимо повідомлення про помилку.
            print("Неправильно введений індекс")

    # Метод, який видаляє існуючу нотатку за її індексом у списку.
    def delete_note(self, index):

        # Перевіряємо, чи є такий індекс у списку нотаток.
        if 0 <= index < len(self.notes):

            self.notes.pop(index)  # Видаляємо нотатку за індексом.
            print("Нотатку видалено")

        else:
            print("Неправильно введений індекс")

    # Метод, який повертає список нотаток, які містять заданий текст у своїх полях.
    def search_by_text(self, text):

        results = []
        for note in self.notes:  # Проходимо по всіх нотатках у нотатнику.

            # Переводимо текст нотатки та запит у нижній регістр.
            note_text = note.text.lower()
            query = text.lower()

            if query in note_text:  # Перевіряємо, чи є запит у тексті нотатки.
                results.append(note)

        return results

    # Метод, що повертає список нотаток, які мають задане ключове слово у своїх полях.
    def search_by_keyword(self, keyword):

        results = []
        for note in self.notes:

            # Переводимо ключове слово та запит у нижній регістр.
            note_keywords = [k.lower() for k in note.keywords]
            query = keyword.lower()

            if query in note_keywords:
                results.append(note)

        return results

    # Метод, який сортує список нотаток за датою створення в порядку зростання або спадання.
    def sort_by_date(self, reverse=False):

        # Використовуємо метод sort для списку нотаток, вказавши ключ сортування та напрямок.
        self.notes.sort(key=lambda note: note.date, reverse=reverse)

    def display_notes(self):

        for i, note in enumerate(self.notes):
            print(f"Індекс:{i}. {note}")

# Клас для зберігання списку нотаток у файл.


class NoteStorage(Notebook):

    def __init__(self):
        super().__init__()

    # Метод, який зберігає список нотаток у pickle файл.
    def save_to_file(self):

        file = None
        for note in self.notes:  # Проходимо по всіх нотатках у нотатнику.
            print(note)

            text = note.text  # Отримуємо текст нотатки.
            words = text.split()  # Розбиваємо текст на слова за пробілами.

            if words:
                # Якщо є хоча б одне слово, то використовуємо перше слово як ім'я файлу.
                file = words[0] + ".pickle"
                break

            else:
                # Якщо немає слів, то використовуємо дату створення нотатки як ім'я файлу.
                file = str(note.date) + ".pickle"
                break

        if file:

            self._save_to_file(file)  # Викликаємо окремий метод для збереження

    # Окремий метод для збереження у файл
    def _save_to_file(self, filename):
        if os.path.exists(filename):
            path_list = filename.split('.')
            filename = path_list[0] + '1.' + path_list[1]
            with open(filename, "wb") as f:
                pickle.dump(self, f)
        else:
            with open(filename, "wb") as f:
                pickle.dump(self, f)

    # Метод, який завантажує список нотаток з файлy.
    def load_from_file(self, filename):

        with open(filename, "rb") as file:

            old_notebook = pickle.load(file)
            for note in old_notebook.notes:
                print(note)
                self.notes.append(note)

    def show_saved_files(self):

        directory = ".\\"  # шлях до каталогу
        extension = ".pickle"  # розширення файлу
        files = []  # список файлів

        # проходимо по всіх елементах у каталозі
        for element in os.listdir(directory):
            # якщо елемент є файлом і має потрібне розширення
            if os.path.isfile(os.path.join(directory, element)) and element.endswith(extension):

                # додаємо ім'я файлу до списку
                files.append(element)

        # виводимо список файлів на екран
        print("Збережені файли:")
        for i, file in enumerate(files):
            print(f"{i + 1} - {file}")

        # повертаємо список файлів
        return files

    # Метод, який видаляє вибраний файл з каталогу.
    def delete_selected_file(self):

        directory = ".\\"
        files = self.show_saved_files()  # отримуємо список файлів

        if files:  # якщо список не пустий

            # зчитуємо номер файлу для видалення
            number = int(input("Введіть номер файлу для видалення: "))

            if 1 <= number <= len(files):  # якщо номер в межах списку

                file = files[number - 1]  # отримуємо ім'я файлу за номером
                # видаляємо файл з каталогу
                os.remove(os.path.join(directory, file))
                print(f"Файл {file} видалено")

            else:
                print("Невірний номер")

        else:
            print("Немає збережених файлів")


class NoteManager:

    def __init__(self):
        self.notebook = Notebook()
        self.notestorage = NoteStorage()

    def menu(self):
        while True:

            # Виводимо меню з можливими діями
            print("Виберіть дію:")
            print("1 - Створити нотатку")
            print("2 - Редагувати нотатку")
            print("3 - Видалити нотатку")
            print("4 - Пошук по тексту")
            print("5 - Пошук за ключовим словом")
            print("6 - Показати створені нотатки")
            print("7 - Сортування по даті створення")
            print("8 - Завантажити нотатку")
            print("9 - Видалити вибраний файл")
            print("10 - Зберегти та вийти")

            choice = input("Ваш вибір: ")

            if choice == "1":

                # Додаємо пропозицію повернутися у цикл вибору
                result = input(
                    "Продовжити (y) чи повернутися у меню вибору (n)? ")
                if result == "n":
                    continue

                else:

                    # Зчитуємо текст нотатки
                    text = input("Введіть текст нотатки: ")
                    keywords = input("Введіть ключові слова нотатки, розділені комами з пробілами: ").split(
                        ",")  # Зчитуємо ключові слова нотатки, розділені комами
                    keywords = [kw.strip(' ')
                                for kw in keywords]  # Видаляємо зайві пробіли
                    # Додаємо нову нотатку
                    self.notebook.add_note(text, keywords)
                    print("Нотатку додано")

            elif choice == "2":

                # Додаємо пропозицію повернутися у цикл вибору
                result = input(
                    "Продовжити (y) чи повернутися у меню вибору (n)? ")
                if result == "n":
                    continue

                else:

                    self.notebook.display_notes()

                    # Зчитуємо індекс нотатки для редагування
                    try:
                        index = int(
                            input("Введіть індекс нотатки для редагування: "))

                    except ValueError:
                        print('Введіть індекс нотатки')

                    # Зчитуємо новий текст нотатки або залишаємо пустим
                    text = input(
                        "Введіть новий текст нотатки чи залиште пустим: ")
                    keywords = input("Введіть нові ключові слова нотатки, розділені комами, чи залиште пустим: ").split(
                        ", ")  # Зчитуємо нові ключові слова нотатки або залишаємо пустим

                    if text or keywords:  # Якщо текст або ключові слова не пусті

                        try:
                            # Редагуємо нотатку за індексом
                            self.notebook.edit_note(index-1, text, keywords)
                            print("Нотатку відредаговано")
                        #  Перехоплюємо помилку з відсутністю нотатки
                        except UnboundLocalError:
                            print(
                                'Нотатки з таким індексом не існує. Створіть нову через пункт 1')

                    else:
                        # Якщо текст і ключові слова пусті, то виводимо повідомлення про помилку
                        print("Немає даних для редагування")

            elif choice == "3":

                # Додаємо пропозицію повернутися у цикл вибору
                result = input(
                    "Продовжити (y) чи повернутися у меню вибору (n)? ")
                if result == "n":
                    continue

                else:

                    self.notebook.display_notes()
                    # Зчитуємо індекс нотатки для видалення
                    index = int(
                        input("Введіть індекс нотатки для видалення: "))
                    # Видаляємо нотатку за індексом
                    self.notebook.delete_note(index-1)

            elif choice == "4":

                # Додаємо пропозицію повернутися у цикл вибору
                result = input(
                    "Продовжити (y) чи повернутися у меню вибору (n)? ")
                if result == "n":
                    continue

                else:
                    # Зчитуємо текст для пошуку
                    text = input("Введіть текст для пошуку: ")
                    results = self.notebook.search_by_text(
                        text)  # Пошук нотаток за текстом
                    # Виводимо кількість знайдених нотаток
                    print(f"Знайдено {len(results)} нотаток:")

                    for note in results:  # Проходимо по всіх знайдених нотатках
                        print(note)  # Виводимо рядкове представлення нотатки

            elif choice == "5":

                # Додаємо пропозицію повернутися у цикл вибору
                result = input(
                    "Продовжити (y) чи повернутися у меню вибору (n)? ")
                if result == "n":
                    continue

                else:

                    # Зчитуємо ключове слово для пошуку
                    keyword = input("Введіть ключове слово для пошуку: ")
                    # Пошук нотаток за ключовим словом
                    results = self.notebook.search_by_keyword(keyword)
                    # Виводимо кількість знайдених нотаток
                    print(f"Знайдено {len(results)} нотаток:")

                    for note in results:  # Проходимо по всіх знайдених нотатках
                        print(note)

            elif choice == "6":

                # Додаємо пропозицію повернутися у цикл вибору
                result = input(
                    "Продовжити (y) чи повернутися у меню вибору (n)? ")
                if result == "n":
                    continue

                else:
                    self.notebook.display_notes()  # Виводить нотатки на екран

            elif choice == "7":

                # Додаємо пропозицію повернутися у цикл вибору
                result = input(
                    "Продовжити (y) чи повернутися у меню вибору (n)? ")
                if result == "n":
                    continue

                else:

                    reverse = int(
                        input("Введіть напрямок сортування (1 - спадання, 0 - зростання): "))
                    # Сортуємо список нотаток за датою створення
                    self.notebook.sort_by_date(reverse)
                    print("Нотатки відсортовано")

            elif choice == "8":

                # Додаємо пропозицію повернутися у цикл вибору
                result = input(
                    "Продовжити (y) чи повернутися у меню вибору (n)? ")
                if result == "n":
                    continue

                else:

                    print(self.notestorage.show_saved_files())

                    filename = input(
                        'Введіть назву файлу без розширення ') + ".pickle"

                    try:
                        # Завантажуємо нотатки з файлу
                        self.notestorage.load_from_file(filename)

                    except FileNotFoundError:
                        print('Файл не знайдено. Спробуйте ввести знову')

            elif choice == "9":

                # Додаємо пропозицію повернутися у цикл вибору
                result = input(
                    "Продовжити (y) чи повернутися у меню вибору (n)? ")
                if result == "n":
                    continue

                else:

                    while True:
                        try:
                            # Видаляємо вибраний файл з каталогу
                            self.notestorage.delete_selected_file()
                            break
                        except ValueError:
                            print("Введіть, будь ласка, номер файлу")
                            continue

            elif choice == "10":

                # Додаємо пропозицію повернутися у цикл вибору
                result = input("Вийти (y) чи повернутися у меню вибору (n)? ")
                if result == "n":
                    continue

                else:

                    if len(self.notebook.notes):

                        # Зберігаємо список нотаток у файл
                        self.notestorage.save_to_file()
                        print("Нотатки збережено")
                        break

                    else:
                        break

            else:
                print("Невірний вибір")


if __name__ == '__main__':
    manager = NoteManager()
    manager.menu()
