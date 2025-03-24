"""Завдання 2

Створіть додаток для приготування пасти. Додаток має вміти створювати щонайменше три види пасти.  Класи різної пасти мають містити такі методи:

    Тип пасти;
    Соус;
    Начинка;
    Добавки.

Для реалізації використовуйте твірні патерни.
"""
from abc import ABC, abstractmethod

# Абстрактний клас Будівельника пасти
class PastaBuilder(ABC):
    def __init__(self):
        self.pasta = Pasta()

    @abstractmethod
    def set_type(self):
        pass

    @abstractmethod
    def set_sauce(self):
        pass

    @abstractmethod
    def set_filling(self):
        pass

    @abstractmethod
    def set_toppings(self):
        pass

    def build(self):
        return self.pasta

# Клас Pasta
class Pasta:
    def __init__(self):
        self.type = None
        self.sauce = None
        self.filling = None
        self.toppings = []

    def __str__(self):
        return (f"Pasta: {self.type}\nSauce: {self.sauce}\nFilling: {self.filling}\n"
                f"Toppings: {', '.join(self.toppings)}")

# Конкретні будівельники для різних видів пасти
class CarbonaraBuilder(PastaBuilder):
    def set_type(self):
        self.pasta.type = "Spaghetti Carbonara"
        return self

    def set_sauce(self):
        self.pasta.sauce = "Creamy egg sauce"
        return self

    def set_filling(self):
        self.pasta.filling = "Bacon"
        return self

    def set_toppings(self):
        self.pasta.toppings = ["Parmesan", "Black pepper"]
        return self

class BologneseBuilder(PastaBuilder):
    def set_type(self):
        self.pasta.type = "Spaghetti Bolognese"
        return self

    def set_sauce(self):
        self.pasta.sauce = "Tomato meat sauce"
        return self

    def set_filling(self):
        self.pasta.filling = "Ground beef"
        return self

    def set_toppings(self):
        self.pasta.toppings = ["Parmesan", "Basil"]
        return self

class PestoBuilder(PastaBuilder):
    def set_type(self):
        self.pasta.type = "Penne Pesto"
        return self

    def set_sauce(self):
        self.pasta.sauce = "Pesto sauce"
        return self

    def set_filling(self):
        self.pasta.filling = "Chicken"
        return self

    def set_toppings(self):
        self.pasta.toppings = ["Pine nuts", "Parmesan"]
        return self

# Директор, що керує створенням пасти
class PastaDirector:
    def __init__(self, builder: PastaBuilder):
        self.builder = builder

    def make_pasta(self):
        return (self.builder.set_type()
                .set_sauce()
                .set_filling()
                .set_toppings()
                .build())

# Тестування
if __name__ == "__main__":
    for builder in [CarbonaraBuilder(), BologneseBuilder(), PestoBuilder()]:
        director = PastaDirector(builder)
        pasta = director.make_pasta()
        print(pasta)
        print("-" * 30)

