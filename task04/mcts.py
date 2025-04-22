from math import sqrt, log
from random import choice
from dots_and_boxes import State


class Node:
    def __init__(self, state: State):
        self.state = state
        self.n = 0
        self.tot_reward = 0
        if not self.is_terminal():
            self.children = {a: None for a in state.all_actions()}

    def __repr__(self):
        s = f"qtot={self.tot_reward} n={self.n} q={self.qvalue():.3f}\n"
        s += "|".join(
            f"{a} {self.children[a].qvalue()}"
            if self.children[a] is not None
            else f"{a} None"
            for a in self.children
        )
        return s + "\n"

    def is_terminal(self):
        return self.state.terminal() != State.ONGOING

    def qvalue(self):
        return self.tot_reward / self.n if self.n > 0 else 0.0

    def update(self, reward):
        self.tot_reward += reward
        self.n += 1

    def expand(self, action, memory):
        cstate = self.state.copy()
        cstate.action(action)
        key = cstate.get_key()
        if key not in memory:
            memory[key] = Node(cstate)
        self.children[action] = memory[key]
        return self.children[action]

    def uct_value(self, action, uct_c):
        if self.children[action] is None:
            return 0.5  # assume draw
        return self.children[action].qvalue() + uct_c * sqrt(
            log(self.n) / self.children[action].n
        )

    def select(self, uct_c):
        if self.state.turn == 0:
            action = max(self.children, key=lambda a: self.uct_value(a, uct_c))
        else:
            action = min(self.children, key=lambda a: self.uct_value(a, -uct_c))
        return self.children[action], action


class MCTSAgent:
    VALUES = [0.0, 1.0, 0.0, 0.5]

    def __init__(self, nrolls=100, uct_c=0.5):
        self.uct_c = uct_c
        self.nrolls = nrolls
        self.memory = {}

    def get_node(self, state):
        key = state.get_key()
        if key not in self.memory:
            self.memory[key] = Node(state)
        return self.memory[key]

    def mcts(self):
        path = []
        node = self.root
        action = None
        while node is not None and not node.is_terminal():
            path.append(node)
            node, action = node.select(self.uct_c)
        if node is None:
            # prosirivanje nodea koristeci zajed. mem.
            node = path[-1].expand(action, self.memory)
            path.append(node)
        cstate = node.state.copy()
        while cstate.terminal() == State.ONGOING:
            action = choice(cstate.all_actions())
            cstate.action(action)
        reward = self.VALUES[cstate.terminal()]
        for n in path:
            n.update(reward)

    def best(self):
        if self.root.state.turn == 0:
            action = max(
                self.root.children,
                key=lambda a: self.root.children[a].qvalue()
                if self.root.children[a]
                else 0.5,
            )
        else:
            action = min(
                self.root.children,
                key=lambda a: self.root.children[a].qvalue()
                if self.root.children[a]
                else 0.5,
            )
        return action, (
            self.root.children[action].qvalue() if self.root.children[action] else 0.5
        )

    def action(self, state: State):
        self.root = self.get_node(state)
        for i in range(self.nrolls):
            self.mcts()

        return self.best()


# if __name__ == "__main__":
#     game = State(3)
#     agent = MCTSAgent()
#     while game.terminal() == State.ONGOING:
#         print(game)
#         action, value = agent.action(game)
#         print(agent.root)
#         print("action:", action, "value:", value)
#         game.action(action)
#     print("game over:", game.terminal())
#     print(game)


if __name__ == "__main__":
    from random import choice

    def play_game(agent_first=True, size=3, nrolls=200):
        game = State(size)
        agent = MCTSAgent(nrolls=nrolls)
        turn = 0  # 0: agent, 1: random
        if not agent_first:
            turn = 1
        while game.terminal() == State.ONGOING:
            # print(game)
            if turn == 0:
                action, value = agent.action(game)
                # print("MCTS agent action:", action, "value:", value)
                game.action(action)
            else:
                action = choice(game.all_actions())
                # print("Random action:", action)
                game.action(action)
            turn = 1 - turn
        # print(game)
        # print("Game over:", game.terminal())
        return game.terminal()

    results = [play_game(agent_first=True) for _ in range(20)]
    results += [play_game(agent_first=False) for _ in range(20)]
    print("Rezultati (1 = agent, 2 = random, 3 = neriseno):", results)
    print("Agent pobjeda:", results.count(1))
    print("Random pobjeda:", results.count(2))
    print("neriseno:", results.count(3))
