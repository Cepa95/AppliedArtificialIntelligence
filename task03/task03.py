from copy import deepcopy


class Stanje:
    def __init__(self, left="VOK", boat="", right="", boatSide="L", lastUnloaded=""):
        self.left = left
        self.boat = boat
        self.right = right
        self.lastUnloaded = lastUnloaded
        self.boatSide = boatSide

    def __repr__(self):
        leftSide = "".join(sorted(self.left, reverse=True)) + (
            "B" if self.boatSide == "L" else ""
        )
        rightSide = "".join(sorted(self.right, reverse=True)) + (
            "B" if self.boatSide == "D" else ""
        )
        return f"left: {leftSide}   right: {rightSide}    => boat: {self.boat} "

    def allActions(self):
        actions = []
        currentSide = self.left if self.boatSide == "L" else self.right

        if self.boat:
            actions.append(self.boat)
        else:
            for obj in currentSide:
                actions.append(obj)

            actions.append("")

        return actions

    def nextStates(self):
        nextStates = []
        currentSide = self.left if self.boatSide == "L" else self.right
        oppositeSide = self.right if self.boatSide == "L" else self.left

        if self.boat:
            newCurrentSide = currentSide + self.boat
            nextStates.append(
                Stanje(
                    newCurrentSide if self.boatSide == "L" else oppositeSide,
                    "",
                    oppositeSide if self.boatSide == "L" else newCurrentSide,
                    self.boatSide,
                )
            )
        else:
            for obj in currentSide:
                newCurrentSide = currentSide.replace(obj, "")
                newBoatSide = "D" if self.boatSide == "L" else "L"
                nextStates.append(
                    Stanje(
                        newCurrentSide if self.boatSide == "L" else oppositeSide,
                        obj,
                        oppositeSide if self.boatSide == "L" else newCurrentSide,
                        newBoatSide,
                    )
                )

            newBoatSide = "D" if self.boatSide == "L" else "L"
            nextStates.append(
                Stanje(
                    currentSide if self.boatSide == "L" else oppositeSide,
                    "",
                    oppositeSide if self.boatSide == "L" else currentSide,
                    newBoatSide,
                )
            )

        return list(nextStates)

    def isSolved(self):
        return (
            "".join(sorted(self.right, reverse=True)) == "VOK" and self.boatSide == "D"
        )

    def isTerminal(self):
        if ("V" in self.left and "O" in self.left and "D" in self.boatSide) or (
            "V" in self.right and "O" in self.right and "L" not in self.boatSide
        ):
            return True
        elif ("O" in self.left and "K" in self.left and "D" in self.boatSide) or (
            "O" in self.right and "K" in self.right and "L" in self.boatSide
        ):
            return True
        elif self.isSolved():
            return True
        elif (
            self.boat == ""
            and not self.isSolved()
            and self.left == "VOK"
            and self.boatSide == "D"
        ):
            return True
        return False

    def action(self, obj):
        if obj:
            if self.boatSide == "L":
                if obj in self.boat:
                    self.boat, self.left, self.lastUnloaded = "", self.left + obj, obj
                else:
                    self.left = self.left.replace(obj, "")
                    self.boat, self.lastUnloaded, self.boatSide = obj, "", "D"
            else:
                if obj in self.boat:
                    self.boat, self.right, self.lastUnloaded = "", self.right + obj, obj
                else:
                    self.right = self.right.replace(obj, "")
                    self.boat, self.lastUnloaded, self.boatSide = obj, "", "L"
        else:
            self.boatSide = "D" if self.boatSide == "L" else "L"
        return self

    def undoAction(self, obj):
        if obj:
            if self.lastUnloaded == obj and not self.boat:
                if self.boatSide == "L":
                    self.left = self.left.replace(obj, "")
                else:
                    self.right = self.right.replace(obj, "")
                self.boat, self.lastUnloaded = obj, ""
            else:
                if self.boatSide == "L":
                    self.right += obj
                    self.boatSide = "D"
                else:
                    self.left += obj
                    self.boatSide = "L"
                self.boat = ""
        else:
            self.boatSide = "D" if self.boatSide == "L" else "L"
        return self

    def copy(self):
        return deepcopy(self)


def generate(startState, dictState):
    state = str(startState)
    if state in dictState:
        return
    if not (
        startState.isTerminal() and startState.boat == "" and not startState.isSolved()
    ) or (startState.left == "VOK" and startState.boatSide == "D"):
        dictState[state] = startState.copy()
    for obj in startState.allActions():
        newState = startState.copy().action(obj)
        generate(newState, dictState)

    return dictState


def solutionBFS(state):
    visited = set()
    queue = [state]
    parents = {str(state): None}

    while queue:
        currentState = queue.pop(0)
        if str(currentState) not in visited:
            visited.add(str(currentState))

            if currentState.isSolved():
                return parents

            if currentState.isTerminal():
                continue

            for nextState in currentState.nextStates():
                if str(nextState) not in visited:
                    queue.append(nextState)
                    parents[str(nextState)] = currentState

    return None


def solutionDFS(state):
    visited = set()
    stack = [state]
    parents = {str(state): None}

    while stack:
        currentState = stack.pop()
        if str(currentState) not in visited:
            visited.add(str(currentState))

            if currentState.isSolved():
                return parents
            
            if currentState.isTerminal():
                continue

            for nextState in currentState.nextStates():
                if str(nextState) not in visited:
                    stack.append(nextState)
                    parents[str(nextState)] = currentState

    return None


def solutionBestFS(state):
    def heuristic(state):
        return sum(1 for char in state.right if char in "VOK")

    queue = [(heuristic(state), state)]
    stateParents = {state: None}
    visited = set()
    while queue:
        queue.sort(key=lambda x: x[0], reverse=True)
        _, currentState = queue.pop(0)
        visited.add(str(currentState))

        if currentState.isSolved():
            return stateParents

        if currentState.isTerminal():
            continue

        for nextState in currentState.nextStates():
            if str(nextState) not in visited:
                visited.add(str(nextState))
                queue.append((heuristic(nextState), nextState))
                stateParents[nextState] = currentState

    return None


if __name__ == "__main__":
    startState = Stanje()
    states = generate(startState, {})
    dfs = solutionDFS(startState)
    bfs = solutionBFS(startState)
    bestFS = solutionBestFS(startState)
    for state in states:
        print(state)
    print("Number of states: ", len(states))

    print()
    print("Dfs:", len(dfs))
    for i in dfs:
        print(i)
    print()
    print("Bfs:", len(bfs))
    for i in bfs:
        print(i)
    print()
    print("BestFS:", len(bestFS))
    for i in bestFS:
        print(i)
