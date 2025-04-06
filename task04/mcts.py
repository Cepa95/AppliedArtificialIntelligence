
from math import sqrt, log
from random import choice
from dots_and_boxes import State

class Node:

    def __init__(self, state: State):
        self.state = state
        self.n = 0
        self.tot_reward = 0
        if not self.is_terminal():
            self.children = { a: None for a in state.all_actions() }
    
    def __repr__(self):
        s = f"qtot={self.tot_reward} n={self.n} q={self.qvalue():.3f}\n"
        s += "|".join(f"{a} {self.children[a].qvalue()}" if self.children[a] is not None else f"{a} None" for a in self.children)
        return s + "\n"
    
    def is_terminal(self):
        return self.state.terminal() != State.ONGOING
    
    def qvalue(self):
        return self.tot_reward / self.n
    
    def update(self, reward):
        self.tot_reward += reward
        self.n += 1
        
    def expand(self, action):
        cstate = self.state.copy()
        cstate.action(action)
        self.children[action] = Node(cstate)
        return self.children[action]
    
    def uct_value(self, action, uct_c):
        if self.children[action] is None:
            return 0.5 # assume draw
        return self.children[action].qvalue() + uct_c * sqrt(log(self.n) / self.children[action].n)
    
    def select(self, uct_c):
        if self.state.turn == 0:
            action = max(self.children, key=lambda a: self.uct_value(a, uct_c))
        else:            
            action = min(self.children, key=lambda a: self.uct_value(a, -uct_c))
        return self.children[action], action
    
class MCTSAgent:

    VALUES = [ 0.0, 1.0, 0.0, 0.5 ]
    
    def __init__(self, nrolls=100, uct_c=0.5):
        self.uct_c = uct_c
        self.nrolls = nrolls

    def mcts(self):
        path = []
        # select until leaf is reached
        node = self.root
        while node is not None and not node.is_terminal():
            path.append(node)
            node, action = node.select(self.uct_c)
        # expand leaf
        if node is None:
            node = path[-1].expand(action)
            path.append(node)
        # random rollout to the end
        cstate = node.state.copy()
        while cstate.terminal() == State.ONGOING:
            action = choice(cstate.all_actions())
            cstate.action(action)
        reward = self.VALUES[cstate.terminal()]
        # update
        for n in path:
            n.update(reward)

    def best(self):
        if self.root.state.turn == 0:
            action = max(self.root.children, key=lambda a: self.root.children[a].qvalue() if self.root.children[a] else 0.5)
        else:            
            action = min(self.root.children, key=lambda a: self.root.children[a].qvalue() if self.root.children[a] else 0.5)
        return action, (self.root.children[action].qvalue() if self.root.children[action] else 0.5)
    
    def action(self, state: State):
        self.root = Node(state)
        for i in range(self.nrolls):
            self.mcts()
        return self.best()

if __name__ == "__main__":
    game = State(3)
    agent = MCTSAgent()
    while game.terminal() == State.ONGOING:
        print(game)
        action, value = agent.action(game)  
        print(agent.root)
        print("action:", action, "value:", value)
        game.action(action)
    print("game over:", game.terminal())
    print(game)
