from spil import Spil
# from player import Igrac, Bot, Human, RandomBot


class Igra:
    def __init__(self, igrac1, igrac2):
        self.igrac1 = igrac1
        self.igrac2 = igrac2
        self.spil = Spil()
        self.igrac1.hand = self.spil.dealHand(5)
        self.igrac2.hand = self.spil.dealHand(5)
        self.odigrane = []
        # self.startingPlayer = random.choice([self.igrac1, self.igrac2])
        self.startingPlayer = igrac1

    def __repr__(self):
        return (
            f"Remaining cards in the deck: {len(self.spil.cards)}\n"
            f"Player 1: {self.igrac1.hand}\nPlayer 2: {self.igrac2.hand}\n"
        )

    def rezultat(self):
        if self.igrac1.wonPictures > self.igrac2.wonPictures:
            return 1
        elif self.igrac1.wonPictures < self.igrac2.wonPictures:
            return 2
        return 0

    def odigraj_ruku(self, prikaz=True):
        firstPlayer = self.startingPlayer
        if firstPlayer == self.igrac2:
            secondPlayer = self.igrac1
        else:
            secondPlayer = self.igrac2

        firstPlayerCard = firstPlayer.hand.pop(
            firstPlayer.akcija(
                {"ruka": firstPlayer.hand, "stol": None, "odigrane": self.odigrane}
            )
        )
        secondPlayerCard = secondPlayer.hand.pop(
            secondPlayer.akcija(
                {
                    "ruka": secondPlayer.hand,
                    "stol": firstPlayerCard,
                    "odigrane": self.odigrane,
                }
            )
        )

        self.odigrane.append((firstPlayerCard, secondPlayerCard))

        if secondPlayerCard[0] % firstPlayerCard[0] == 0:
            winner = firstPlayer
        elif firstPlayerCard[0] % secondPlayerCard[0] == 0:
            winner = secondPlayer
        else:
            winner = firstPlayer

        if winner == firstPlayer:
            winner.wonPictures += int(firstPlayerCard[0] in [11, 12, 13])

        else:
            winner.wonPictures += int(secondPlayerCard[0] in [11, 12, 13])

        if prikaz:
            print(
                f"{firstPlayer.name} plays {firstPlayerCard}, {secondPlayer.name} plays {secondPlayerCard} - {winner.name} wins"
            )

        if self.spil.cards:
            winner.hand.append(self.spil.splitCard())
            if winner == secondPlayer:
                firstPlayer.hand.append(self.spil.splitCard())
            else:
                secondPlayer.hand.append(self.spil.splitCard())

        self.startingPlayer = winner

    def odigraj_partiju(self, prikaz=True):
        while self.spil.cards or (self.igrac1.hand and self.igrac2.hand):
            self.odigraj_ruku(prikaz)
        rezultat = self.rezultat()
        if prikaz:
            print(f"Final result: {rezultat}")
        return rezultat


# if __name__ == "__main__":
#     while True:
#         igrac1 = Human("Čovjek")
#         igrac2 = Bot("Računalo")
#         igra = Igra(igrac1, igrac2)
#         print(igra)
#         igra.odigraj_partiju(prikaz=True)

#         newGame = input("Do you want to start a new game? (yes/no): ").strip().lower()
#         if newGame != "yes":
#             break
