import random


class Igrac:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.wonPictures = 0

    def akcija(self, stanje):
        return random.randint(0, len(self.hand) - 1)


class Human(Igrac):
    def akcija(self, stanje):
        while True:
            try:
                print(f"Your cards: {self.hand}")
                choice = int(input("Select card index: "))
                if 0 <= choice < len(self.hand):
                    return choice
                else:
                    print("Invalid index. Try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")


class Bot(Igrac):
    def isPrime(self, num):
        if num <= 1:
            return False
        for i in range(2, int(num**0.5) + 1):
            if num % i == 0:
                return False
        return True

    def akcija(self, stanje):
        stol = stanje.get("stol")

        if stol:
            for i, card in enumerate(self.hand):
                if stol[0] % card[0] == 0 and stol[0] in [11, 12, 13]:
                    return i

            for i, card in enumerate(self.hand):
                if stol[0] % card[0] == 0:
                    return i

        for i, card in enumerate(self.hand):
            if self.isPrime(card[0]):
                return i

        for i, card in enumerate(self.hand):
            if card[0] in [11, 12, 13]:
                return i

        return min(range(len(self.hand)), key=lambda i: self.hand[i][0])


class RandomBot(Igrac):
    def akcija(self, stanje):
        return random.randint(0, len(self.hand) - 1)
