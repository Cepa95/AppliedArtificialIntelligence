# from dots_and_boxes import State
# from minimax import MinimaxAgent
# from mcts import MCTSAgent
# from randombot import RandomAgent
# game_size = 3

# def match(agent1, agent2, show=False):
#     game = State(game_size)
#     while True:
#         action, value = agent1.action(game)  
#         if show:
#             print(game, action, value)
#         game.action(action)
#         if game.terminal() != State.ONGOING:
#             return game.terminal()
#         action, value = agent2.action(game)  
#         if show:
#             print(game, action, value)
#         game.action(action)
#         if game.terminal() != State.ONGOING:
#             return game.terminal()

# def compare(agent1, agent2, ntimes):
#     score = [ 0, 0 ]
#     agent1.memory = {}
#     for i in range(ntimes):
#         print(score)
#         if i % 2 == 0:
#             rez = match(agent1, agent2)
#             if rez == State.P1_WON:
#                 score[0] += 1
#             elif rez == State.P2_WON:
#                 score[1] += 1
#             else:
#                 score[0] += 0.5
#                 score[1] += 0.5
#         else:
#             rez = match(agent2, agent1)
#             if rez == State.P1_WON:
#                 score[1] += 1
#             elif rez == State.P2_WON:
#                 score[0] += 1
#             else:
#                 score[0] += 0.5
#                 score[1] += 0.5
#     return score

# agent1 = MinimaxAgent(1)
# agent2 = MCTSAgent(200) 
# agent3 = RandomAgent()
# score = compare(agent2, agent3, 1000)


from dots_and_boxes import State
from minimax import MinimaxAgent
from mcts import MCTSAgent
from randombot import RandomAgent
game_size = 3

def match(agent1, agent2, show=False):
    game = State(game_size)
    agents = [agent1, agent2]
    turn = 0
    while game.terminal() == State.ONGOING:
        if show:
            print(game)
        action, _ = agents[turn].action(game)
        game.action(action)
        turn = 1 - turn 
    if show:
        print(game)
        print("Game over:", game.terminal())
    return game.terminal()


# def match(agent1, agent2, show=False):
#     game = State(game_size)
#     while True:
#         action, value = agent1.action(game)  
#         if show:
#             print(game, action, value)
#         game.action(action)
#         if game.terminal() != State.ONGOING:
#             return game.terminal()
#         action, value = agent2.action(game)  
#         if show:
#             print(game, action, value)
#         game.action(action)
#         if game.terminal() != State.ONGOING:
#             return game.terminal()


def compare(agent1_class, agent2_class, ntimes, agent1_kwargs=None, agent2_kwargs=None):
    score = [0, 0]
    agent1_kwargs = agent1_kwargs or {}
    agent2_kwargs = agent2_kwargs or {}
    for i in range(ntimes):
        print(score)
        agent1 = agent1_class(**agent1_kwargs)
        agent2 = agent2_class(**agent2_kwargs)
        if i % 2 == 0:
            rez = match(agent1, agent2) 
            if rez == State.P1_WON:
                score[0] += 1
            elif rez == State.P2_WON:
                score[1] += 1
            else:
                score[0] += 0.5
                score[1] += 0.5
        else:
            rez = match(agent2, agent1) 
            if rez == State.P1_WON: 
                score[1] += 1
            elif rez == State.P2_WON: 
                score[0] += 1
            else:
                score[0] += 0.5
                score[1] += 0.5
    return score


score = compare(
    MCTSAgent, RandomAgent, 1000, 
    agent1_kwargs={'nrolls': 200, 'uct_c': 0.5}, 
    agent2_kwargs={}
)
# score = compare(
#     MCTSAgent, MinimaxAgent, 1000, 
#     agent1_kwargs={'nrolls': 200, 'uct_c': 0.5}, 
#     agent2_kwargs={'maxdepth': 1}
# )
print(score)