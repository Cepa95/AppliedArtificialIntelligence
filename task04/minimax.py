from dots_and_boxes import State


class MinimaxAgent:
    VALUES = [0, 100, -100, 0]

    def __init__(self, maxdepth=4):
        self.maxdepth = maxdepth
        self.nodes = 0
        self.transposition_table = {}

    def score(self, state):
        """Vraca trenutnu razliku bodova."""
        return len(state.boxes[0]) - len(state.boxes[1])

    def sorted_actions(self, state):
        """Sortira poteze prema broju zatvorenih kvadrata."""
        actions = state.all_actions()

        def count_closed_boxes(action):
            # Raspakiraj početnu i krajnju točku linije
            (xf, yf), (xt, yt) = action
            # Izračunaj broj zatvorenih kvadrata za ovu liniju
            return len(state.closed_boxes(xf, yf, xt, yt))

        # Sortiraj akcije prema broju zatvorenih kvadrata (najveći broj prvo)
        return sorted(actions, key=count_closed_boxes, reverse=True)

    def minimax(self, state, alpha, beta, depth):
        self.nodes += 1
        state_key = str(state)

        # Provjera transpozicijske tablice
        if state_key in self.transposition_table:
            entry = self.transposition_table[state_key]
            if entry["depth"] >= depth and entry["is_exact"]:
                return entry["best_action"], entry["value"]
            best_action = entry["best_action"]
        else:
            best_action = None

        if state.terminal() != State.ONGOING:
            return None, self.VALUES[state.terminal()]
        if depth == 0:
            return None, self.score(state)

        best = None
        if state.turn == 0:  # Maximizirajući igrač
            for action in self.sorted_actions(state):
                if (
                    action == best_action
                ):  # Ako postoji najbolja akcija iz tablice, isprobaj je prvu
                    continue
                state.action(action)
                _, value = self.minimax(state, alpha, beta, depth - 1)
                state.undo(action)
                if value > alpha:
                    alpha = value
                    best = action
                if alpha >= beta:
                    break
            value = alpha
        else:  # Minimizirajući igrač
            for action in self.sorted_actions(state):
                if (
                    action == best_action
                ):  # Ako postoji najbolja akcija iz tablice, isprobaj je prvu
                    continue
                state.action(action)
                _, value = self.minimax(state, alpha, beta, depth - 1)
                state.undo(action)
                if value < beta:
                    beta = value
                    best = action
                if alpha >= beta:
                    break
            value = beta

        # Spremanje u transpozicijsku tablicu
        if best_action is not None:
            self.transposition_table[state_key] = {
                "best_action": best,
                "value": value,
                "depth": depth,
                "is_exact": alpha < beta,
            }

        return best, value

    def action(self, state: State):
        self.nodes = 0
        return self.minimax(state, -1000, 1000, self.maxdepth)


if __name__ == "__main__":
    game = State(5)
    agent = MinimaxAgent(6)
    while game.terminal() == State.ONGOING:
        print(game)
        action, value = agent.action(game)
        print("action:", action, "value:", value, "nodes", agent.nodes)
        game.action(action)
    print("game over:", game.terminal())
    print(game)
