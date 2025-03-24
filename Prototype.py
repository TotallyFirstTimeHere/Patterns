"""Реалізуйте патерн Prototype. Протестуйте роботу створеного класу."""

import copy

# Клас, що підтримує прототипне клонування
class Computer:
    def __init__(self, cpu, ram, storage):
        self.cpu = cpu
        self.ram = ram
        self.storage = storage

    def clone(self):
        return copy.deepcopy(self)

    def __str__(self):
        return f"Computer with CPU: {self.cpu}, RAM: {self.ram}, Storage: {self.storage}"


# Тестування патерну Prototype
if __name__ == "__main__":
    original_computer = Computer("Intel i7", "16GB", "512GB SSD")
    cloned_computer = original_computer.clone()

    print("Original:", original_computer)
    print("Cloned:", cloned_computer)

    # Перевіримо, що це різні об'єкти
    print("Objects are the same:", original_computer is cloned_computer)
