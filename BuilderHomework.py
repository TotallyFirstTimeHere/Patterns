"""Завдання 1

Реалізуйте патерн Builder. Протестуйте роботу створеного класу."""

class Computer:
    def __init__(self):
        self.cpu = None
        self.ram = None
        self.storage = None

    def __str__(self):
        return f"Computer with CPU: {self.cpu}, RAM: {self.ram}, Storage: {self.storage}"


class ComputerBuilder:
    def __init__(self):
        self.computer = Computer()

    def set_cpu(self, cpu):
        self.computer.cpu = cpu
        return self

    def set_ram(self, ram):
        self.computer.ram = ram
        return self

    def set_storage(self, storage):
        self.computer.storage = storage
        return self

    def build(self):
        return self.computer


# Тестування патерну Builder
if __name__ == "__main__":
    builder = ComputerBuilder()
    custom_computer = builder.set_cpu("Intel i9").set_ram("32GB").set_storage("1TB SSD").build()
    print(custom_computer)
