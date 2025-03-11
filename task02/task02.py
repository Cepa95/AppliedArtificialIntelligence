import random


class Spil:
    def __init__(self):
        self.cards = self.generateDeck()

    def generateDeck(self):
        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
        colors = ["Black", "Blue", "Green", "Red"]
        deck = []
        for num in numbers:
            for color in colors:
                deck.append((num, color))
        random.shuffle(deck)

        return deck

    def splitCards(self, numOfCards):
        hand =  []
        for i in range(numOfCards):
            if self.cards:
                hand.append(self.cards.pop())
        return hand


spil = Spil()
print(spil.generateDeck())
