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

    def splitCard(self):
        if self.cards:
            return self.cards.pop()
        return None

    def dealHand(self, numOfCards):
        hand = []
        for i in range(numOfCards):
            hand.append(self.splitCard())
        return hand