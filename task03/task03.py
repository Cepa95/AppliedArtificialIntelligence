from copy import deepcopy


class Stanje:
    def __init__(self, initialStart):
        self.left, self.right = initialStart.split("  ||  ")
        self.boat = "left"
        self.boatContents = ""

    def __str__(self):
        return f"{self.left}  ||  {self.right}  => Boat is {self.boat} -> BoatContents: {self.boatContents}"

    def allActions(self):
        nextState = []
        validationLst = ["V", "O", "K", "B"]

        if self.boat == "left":
            for i in validationLst:
                if i in self.left:
                    nextState.append(i)
        else:
            for i in validationLst:
                if i in self.right:
                    nextState.append(i)

        return nextState

    def nextStates(self):
        state = []

        for i in self.allActions():
            tmp = self.copy()
            tmp.action(i)
            state.append(tmp)

        return state

    def isSolved(self):
        if self.left != "----":
            return False
        validationLst = ["V", "O", "K", "B"]
        for char in validationLst:
            if char not in self.right:
                return False
        return True

    def isTerminal(self):
        if ("V" in self.left and "O" in self.left and "B" not in self.left) or (
            "V" in self.right and "O" in self.right and "B" not in self.right
        ):
            return True
        elif ("O" in self.left and "K" in self.left and "B" not in self.left) or (
            "O" in self.right and "K" in self.right and "B" not in self.right
        ):
            return True
        elif self.isSolved():
            return True
        return False

    def move(self, act, fromSide, toSide):
        fromSide = fromSide.replace(act, "-", 1).replace("B", "-", 1)
        toSide = toSide.replace("-", act, 1).replace("-", "B", 1)
        return fromSide, toSide

    def cleanUp(self):
        while self.left.count("B") > 1:
            self.left = self.left.replace("B", "-", 1)
        while self.right.count("B") > 1:
            self.right = self.right.replace("B", "-", 1)

    def undoAction(self, act):
        if self.boat == "right":
            self.right, self.left = self.move(act, self.right, self.left)
            self.boat = "left"
        else:
            self.left, self.right = self.move(act, self.left, self.right)
            self.boat = "right"

        self.boatContents = act  # za algoritme, ako bude tribalo
        self.cleanUp()
        return self.left, self.right

    def action(self, act):
        self.boatContents = act  # isto
        if self.boat == "left":
            self.left, self.right = self.move(act, self.left, self.right)
            self.boat = "right"
        else:
            self.right, self.left = self.move(act, self.right, self.left)
            self.boat = "left"

        self.cleanUp()

    def copy(self):
        return deepcopy(self)


def sortState(state):
    sortLeft = "".join(sorted(state.left))
    sortRight = "".join(sorted(state.right))
    return f"{sortLeft} || {sortRight} => Boat is {state.boat} || BoatContents: {state.boatContents}"


# def generate(state):
#     visited = set()
#     stack = [state]

#     while stack:
#         currentState = stack.pop()
#         sortedState = sortState(currentState)

#         if sortedState in visited:
#             continue

#         # if currentState.isTerminal():
#         #      continue

#         print(currentState)
#         # print(sortedState)
#         visited.add(sortedState)

#         if currentState.isTerminal():
#             continue

#         for action in currentState.allActions():
#             nextState = currentState.copy()
#             nextState.action(action)
#             stack.append(nextState)

#     return


def generate(state, stateGraph, visited):
    sortedState = sortState(state)
    if sortedState in visited:
        return

    visited.add(str(sortedState))
    stateGraph[str(state)] = state.copy()

    for action in state.allActions():
        nextState = state.copy()
        nextState.boatContents = action
        nextState.action(action)
        generate(nextState, stateGraph, visited)
        nextState.undoAction(action)
        nextState.boatContents = ""

    return stateGraph


def solutionDFS(state):
    stack = [state]
    stateParents = {str(state): None}
    visited = set()

    while stack:
        currentState = stack.pop()
        visited.add(str(currentState))

        if currentState.isSolved():
            path = []
            while currentState is not None:
                path.append(str(currentState))
                currentState = stateParents[str(currentState)]
            path.reverse()
            for st in path:
                print(st)

            # for st, parent in stateParents.items():
            #     print(f"state: {st} : parent: {parent}")
            return

        if currentState.isTerminal():
            continue

        for nextState in currentState.nextStates():
            if str(nextState) not in visited:
                stack.append(nextState)
                stateParents[str(nextState)] = str(currentState)

    return None


def solutionBFS(state):
    queue = [state]
    stateParents = {str(state): None}
    visited = set()

    while queue:
        currentState = queue.pop(0)
        visited.add(str(currentState))

        if currentState.isSolved():
            path = []
            while currentState is not None:
                path.append(str(currentState))
                currentState = stateParents[str(currentState)]
            path.reverse()
            for st in path:
                print(st)
            return

        if currentState.isTerminal():
            continue

        for nextState in currentState.nextStates():
            if str(nextState) not in visited:
                queue.append(nextState)
                stateParents[str(nextState)] = str(currentState)

    return None


def heuristic(state):
    return sum(1 for char in state.right if char in "VOK")


def BestFS(state):
    queue = [state]
    stateParents = {str(state): None}
    visited = set()

    while queue:
        queue.sort(key=heuristic, reverse=True)
        currentState = queue.pop(0)
        visited.add(str(currentState))

        if currentState.isSolved():
            path = []
            while currentState is not None:
                path.append(str(currentState))
                currentState = stateParents[str(currentState)]
            path.reverse()
            for st in path:
                print(st)

            return path

        if currentState.isTerminal():
            continue

        for nextState in currentState.nextStates():
            if str(nextState) not in visited:
                queue.append(nextState)
                stateParents[str(nextState)] = str(currentState)

    return None


if __name__ == "__main__":
    state = Stanje("VOKB  ||  ----")

    # generate(state)
    stateGraph = generate(state, {}, set())
    for key, value in stateGraph.items():
        print(f"{key}")

    print("\nDFS solution:")
    solutionDFS(state)

    print("\nBFS solution:")
    solutionBFS(state)

    print("\nBestFS solution:")
    BestFS(state)
