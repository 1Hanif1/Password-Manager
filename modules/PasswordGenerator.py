import random


class PasswordGenerator():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
               'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    def __init__(self):

        nr_letters = random.randint(8, 10)
        nr_symbols = random.randint(2, 4)
        nr_numbers = random.randint(2, 4)

        self.password = self.generatePassword(
            nr_letters, nr_symbols, nr_numbers)

    def generatePassword(self, num_letters, num_symbols, num_numbers) -> str:
        password = ""
        for _ in range(num_letters):
            password += self.letters[random.randint(0, len(self.letters) - 1)]

        for _ in range(num_symbols):
            password += self.symbols[random.randint(0, len(self.symbols) - 1)]

        for _ in range(num_numbers):
            password += self.numbers[random.randint(0, len(self.numbers) - 1)]

        password = self.randomisePassword(password)
        return password

    def randomisePassword(self, password) -> str:
        randomised_password = ""
        password_chars = [char for char in password]
        random.shuffle(password_chars)
        for char in password_chars:
            randomised_password += char
        return randomised_password

    def get_password(self):
        return self.password
