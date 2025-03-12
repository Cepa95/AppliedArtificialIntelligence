from game import Igra
from player import Bot, RandomBot

def playGames(agent1, agent2, N):
    agent1wins = 0
    agent2Wins = 0

    for i in range(N):
        igra = Igra(agent1, agent2) if i < N / 2 else Igra(agent2, agent1)
        result = igra.odigraj_partiju(prikaz=False)
        
        if (i < N / 2 and result == 1) or (i >= N / 2 and result == 2):
            agent1wins += 1
        elif (i < N / 2 and result == 2) or (i >= N / 2 and result == 1):
            agent2Wins += 1

    return agent1wins, agent2Wins

if __name__ == "__main__":
    N = 100 
    agent1 = Bot("Bot")
    agent2 = RandomBot("RandomBot")

    agent1wins, agent2Wins = playGames(agent1, agent2, N)

    print(f"Agent 1 (Bot) wins: {agent1wins}")
    print(f"Agent 2 (RandomBot) wins: {agent2Wins}")
    print(f"Agent 1 (Bot) win percentage: {agent1wins / N * 100:.2f}%")
    print(f"Agent 2 (RandomBot) win percentage: {agent2Wins / N * 100:.2f}%")

    if agent1wins / N > 0.7:
        print("Agent 1 (Bot) wins more than 70% of the games.")
    if agent2Wins / N > 0.7:
        print("Agent 2 (RandomBot) wins more than 70% of the games.")