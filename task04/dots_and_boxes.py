class State:
    ONGOING = 0
    P1_WON = 1
    P2_WON = 2
    DRAW = 3

    def __init__(self, size=5):
        self.size = size  # veličina table (u točkama)
        self.lines = (
            set()
        )  # sve odigrane linije ((x1, y1), (x2, y2)) i obrnuto ((x2, y2), (x1, y1))
        self.boxes = [
            set(),
            set(),
        ]  # gornji lijevi vrhovi zatvorenih kvadrata za p1 i p2, do trenutnog stanja ((x1, y1), (x2, y2))
        self.turn = 0  # igrač na redu 0 = p1, 1 = p2
        self.step = 0  # broj (polu)poteza do ovog stanja
        self.stack = []  # stog na koji će se pamtiti koji igrač je bio na redu pri poništavanju poteza

    def __repr__(self):
        board = []
        for y in range(self.size):
            row = []
            for x in range(self.size):
                row.append("o")
                if x < self.size - 1:
                    row.append("\u23af" if ((x, y), (x + 1, y)) in self.lines else " ")
            board.append(row)
            if y < self.size - 1:
                row = []
                for x in range(self.size):
                    row.append("|" if ((x, y), (x, y + 1)) in self.lines else " ")
                    if x < self.size - 1:
                        if (x, y) in self.boxes[0]:
                            row.append("0")
                        elif (x, y) in self.boxes[1]:
                            row.append("1")
                        else:
                            row.append("\u25a1")
                board.append(row)
        s = f"step: {self.step} turn: " + ("p2" if self.turn == 1 else "p1") + "\n"
        s += "\n".join(" ".join(row) for row in board)
        s += (
            "\nscore: " + str(len(self.boxes[0])) + " " + str(len(self.boxes[1])) + "\n"
        )
        return s + "\n"

    def get_key(self):
        """Generira jedinstveni string key za trenutno stanje igre."""
        # Pretvori linije u sortiranu listu i zatim u string
        lines_key = ",".join(
            f"{line[0]}-{line[1]}"
            for line in sorted(set(tuple(sorted(line)) for line in self.lines))
        )
        # Pretvori zatvorene kvadrate u sortirane stringove
        boxes_key_p1 = ",".join(f"{box}" for box in sorted(self.boxes[0]))
        boxes_key_p2 = ",".join(f"{box}" for box in sorted(self.boxes[1]))
        return f"lines:{lines_key}|boxes_p1:{boxes_key_p1}|boxes_p2:{boxes_key_p2}|turn:{self.turn}|step:{self.step}"

    def copy(self):
        cstate = State(self.size)
        cstate.lines = self.lines.copy()
        cstate.boxes = [self.boxes[0].copy(), self.boxes[1].copy()]
        cstate.turn = self.turn
        cstate.step = self.step
        cstate.stack = self.stack.copy()
        return cstate

    def valid_from(self, x, y):
        vto = []
        for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            if (
                0 <= x + dx < self.size
                and 0 <= y + dy < self.size
                and ((x, y), (x + dx, y + dy)) not in self.lines
            ):
                vto.append((x + dx, y + dy))
        return vto

    def all_actions(self):
        actions = set()
        for xf in range(self.size):
            for yf in range(self.size):
                for xt, yt in self.valid_from(xf, yf):
                    if ((xt, yt), (xf, yf)) not in actions:
                        actions.add(((xf, yf), (xt, yt)))
        return list(actions)

    def closed_boxes(self, xf, yf, xt, yt):
        boxes = set()
        if yf == yt:
            if (
                ((xf, yf - 1), (xt, yf - 1)) in self.lines
                and ((xf, yf), (xf, yf - 1)) in self.lines
                and ((xt, yt), (xt, yf - 1)) in self.lines
            ):
                boxes.add((xf, yf - 1))
            if (
                ((xf, yf + 1), (xt, yf + 1)) in self.lines
                and ((xf, yf), (xf, yf + 1)) in self.lines
                and ((xt, yt), (xt, yf + 1)) in self.lines
            ):
                boxes.add((xf, yf))
        else:  # xf == xt
            if (
                ((xf - 1, yf), (xf - 1, yt)) in self.lines
                and ((xf, yf), (xf - 1, yf)) in self.lines
                and ((xt, yt), (xf - 1, yt)) in self.lines
            ):
                boxes.add((xf - 1, yf))
            if (
                ((xf + 1, yf), (xf + 1, yt)) in self.lines
                and ((xf, yf), (xf + 1, yf)) in self.lines
                and ((xt, yt), (xf + 1, yt)) in self.lines
            ):
                boxes.add((xf, yf))
        return boxes

    def action(self, act):
        """Izvrsava potez i azurira stanje."""
        (xf, yf), (xt, yt) = act
        self.lines.add(((xf, yf), (xt, yt)))
        self.lines.add(((xt, yt), (xf, yf)))
        closed = self.closed_boxes(xf, yf, xt, yt)
        self.boxes[self.turn].update(closed)
        self.stack.append(self.turn)
        self.step += 1
        if not closed:
            self.turn = 1 - self.turn  # Promjena reda igrača

    def undo(self, act):
        """Ponistava potez i vraca stanje na prethodno."""
        (xf, yf), (xt, yt) = act
        self.lines.remove(((xf, yf), (xt, yt)))
        self.lines.remove(((xt, yt), (xf, yf)))
        closed = self.closed_boxes(xf, yf, xt, yt)
        self.boxes[self.stack.pop()].difference_update(closed)
        self.step -= 1
        if not closed:
            self.turn = 1 - self.turn

    def terminal(self):
        if self.step == self.size * (self.size - 1) * 2:
            if len(self.boxes[0]) > len(self.boxes[1]):
                return self.P1_WON
            elif len(self.boxes[0]) < len(self.boxes[1]):
                return self.P2_WON
            else:
                return self.DRAW
        return self.ONGOING


if __name__ == "__main__":
    from random import choice

    def random_test(game):
        if game.terminal() != State.ONGOING:
            print(game)
            print("game over:", game.terminal())
            return
        bstr = str(game)
        actions = game.all_actions()
        print(game)
        act = choice(actions)
        print("action:", act)
        game.action(act)
        random_test(game)
        game.undo(act)
        astr = str(game)
        assert bstr == astr

    game = State(5)
    random_test(game)
