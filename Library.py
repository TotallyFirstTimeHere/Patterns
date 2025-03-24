import json
import logging
import sys
from abc import ABC, abstractmethod
from typing import List

# Налаштування логування
logging.basicConfig(filename='library.log', level=logging.INFO, format='%(asctime)s - %(message)s')


# Патерн Prototype
class Prototype(ABC):
    @abstractmethod
    def clone(self):
        pass


# Сутності
class Book(Prototype):
    def __init__(self, title: str, author: str, year: int):
        self.title = title
        self.author = author
        self.year = year

    def __str__(self):
        return f"{self.title} by {self.author}, {self.year}"

    def clone(self):
        return Book(self.title, self.author, self.year)


# Фабрика користувачів
class UserFactory:
    @staticmethod
    def create_user(user_type: str, name: str):
        if user_type == "Librarian":
            return Librarian(name)
        elif user_type == "Reader":
            return Reader(name)
        else:
            raise ValueError("Unknown user type")


class User(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def get_role(self) -> str:
        pass

    def __str__(self):
        return f"{self.get_role()}: {self.name}"


class Librarian(User):
    def get_role(self):
        return "Librarian"


class Reader(User):
    def get_role(self):
        return "Reader"


# Менеджер бібліотеки (Сінглтон + Фасад)
class LibraryManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.books: List[Book] = []
            cls._instance.users: List[User] = []
        return cls._instance

    def add_book(self, book: Book):
        self.books.append(book)
        logging.info(f"Added book: {book}")

    def remove_book(self, title: str):
        initial_length = len(self.books)
        self.books = [book for book in self.books if book.title != title]
        if len(self.books) < initial_length:
            logging.info(f"Removed book: {title}")
        else:
            logging.warning(f"Book not found: {title}")

    def edit_book(self, old_title: str, new_book: Book):
        for i, book in enumerate(self.books):
            if book.title == old_title:
                self.books[i] = new_book
                logging.info(f"Edited book: {old_title} -> {new_book}")
                return
        logging.warning(f"Book not found: {old_title}")

    def add_user(self, user: User):
        self.users.append(user)
        logging.info(f"Added user: {user}")

    def search_book(self, keyword: str) -> List[Book]:
        return [book for book in self.books if keyword.lower() in book.title.lower()]

    def save_to_file(self, filename: str):
        data = {
            "books": [{"title": book.title, "author": book.author, "year": book.year} for book in self.books],
            "users": [{"name": user.name, "role": user.get_role()} for user in self.users]
        }

        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        logging.info(f"📚 Дані бібліотеки збережено у файл: {filename}")
        print(f"✅ Дані бібліотеки успішно збережено у файл {filename}.")

    def load_from_file(self, filename: str):
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                data = json.load(file)

                # Завантажуємо книги
                self.books = [Book(**book) for book in data.get("books", [])]

                # Завантажуємо користувачів
                self.users = [UserFactory.create_user(user["role"], user["name"]) for user in data.get("users", [])]

            logging.info(f"📂 Дані бібліотеки завантажено з файлу: {filename}")
            print(f"✅ Дані бібліотеки успішно завантажено з файлу {filename}.")

        except FileNotFoundError:
            logging.error(f"❌ Файл {filename} не знайдено.")
            print(f"⚠️ Помилка: Файл {filename} не знайдено.")
        except Exception as e:
            logging.error(f"❌ Помилка при завантаженні файлу {filename}: {e}")
            print(f"⚠️ Помилка: Неможливо прочитати файл {filename}. Деталі: {e}")


# Вхід та реєстрація користувачів
def login_or_register():
    library = LibraryManager()

    while True:
        print("\n1. Увійти")
        print("2. Зареєструватися")
        choice = input("Ваш вибір: ").strip()

        if choice == "1":  # Вхід
            name = input("Введіть ім'я: ").strip()
            for user in library.users:
                if user.name.lower() == name.lower():
                    print(f"Вхід успішний. Вітаємо, {user.name}!")
                    return user
            print("Користувача не знайдено. Спробуйте ще раз або зареєструйтесь.")

        elif choice == "2":  # Реєстрація
            name = input("Введіть ім'я: ").strip()
            role = input("Тип акаунту (Librarian/Reader): ").strip().lower()  # Переводимо у нижній регістр
            if role not in ["librarian", "reader"]:
                print("❌ Невірний тип користувача. Введіть Librarian або Reader.")
                continue

            role = role.capitalize()  # Перетворюємо в "Librarian" або "Reader"
            user = UserFactory.create_user(role, name)
            library.add_user(user)
            print(f"✅ Акаунт створено! Вітаємо, {user.name} ({user.get_role()})!")
            return user

        else:
            print("❌ Невірний вибір, спробуйте ще раз.")


# Меню користувача
def menu():
    library = LibraryManager()
    library.load_from_file("library.json")

    user = login_or_register()

    running = True  # Змінна для контролю виходу

    while running:
        print("\nМеню:")
        print("1. Пошук книги")
        if user.get_role() == "Librarian":
            print("2. Додати книгу")
            print("3. Видалити книгу")
            print("4. Редагувати книгу")
            print("5. Зберегти в файл")
            print("6. Завантажити з файлу")
        print("7. Вийти")

        choice = input("Ваш вибір: ")

        try:
            if choice == "1":
                keyword = input("Ключове слово для пошуку: ")
                results = library.search_book(keyword)
                if results:
                    print("Результати пошуку:")
                    for book in results:
                        print(book)
                else:
                    print("Книг за цим запитом не знайдено.")

            elif choice == "7":  # ВИХІД для ВСІХ користувачів
                library.save_to_file("library.json")
                print("✅ Дані збережено. До побачення!")
                running = False  # Вихід з циклу

            elif user.get_role() == "Librarian":  # Додаткові опції лише для бібліотекаря
                if choice == "2":
                    title = input("Назва: ")
                    author = input("Автор: ")
                    while True:
                        try:
                            year = int(input("Рік: "))
                            break
                        except ValueError:
                            print("Помилка: Введіть число для року.")
                    library.add_book(Book(title, author, year))

                elif choice == "3":
                    title = input("Назва книги для видалення: ")
                    library.remove_book(title)

                elif choice == "4":
                    old_title = input("Назва книги для редагування: ")
                    new_title = input("Нова назва: ")
                    new_author = input("Новий автор: ")
                    while True:
                        try:
                            new_year = int(input("Новий рік: "))
                            break
                        except ValueError:
                            print("Помилка: Введіть число для року.")
                    library.edit_book(old_title, Book(new_title, new_author, new_year))

                elif choice == "5":
                    library.save_to_file("library.json")

                elif choice == "6":
                    library.load_from_file("library.json")

            else:
                print("❌ Невірний вибір, спробуйте ще раз.")

        except Exception as e:
            logging.error(f"Unhandled exception: {e}")
            print(f"Помилка: {e}")


# Запуск програми
if __name__ == "__main__":
    library = LibraryManager()
    menu()
