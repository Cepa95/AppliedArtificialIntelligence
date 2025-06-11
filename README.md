# AppliedArtificialIntelligence

OSS Split

dr. sc. Toma Rončević

Year 2024./2025.


## 📁 Contents

1. [Two-Player Card Game with Agents](#1-two-player-card-game-with-agents)
2. [Wolf, Sheep, Cabbage Puzzle - Informed Search](#2-wolf-sheep-cabbage-puzzle---informed-search)
3. [Dots and Boxes - Minimax & MCTS](#3-dots-and-boxes---minimax--mcts)

---
## 1. ♠️ Two-Player Card Game with Agents

### Game Rules:
- Each player starts with 5 cards from a standard deck (52 cards).
- **Goal**: Win more "picture cards" (J, Q, K = 11, 12, 13).
- In each round:
  - One player plays a card; the other responds.
  - Winning logic:
    - A card that divides the other wins (e.g., 3 beats 6).
    - If no division, first player wins.
    - If equal cards, second player wins.
- Players draw new cards after each round.
- Game ends when all cards are played.

---

## 3. 🧠 Wolf, Sheep, and Cabbage Puzzle - Informed Search

A classic river-crossing puzzle implemented as a **graph search problem**.

- **State Representation**: Object positions and boat side
- **Invalid States**: Left wolf and sheep, or sheep and cabbage unsupervised
- **Goal**: Safely transfer all to the opposite side

Implemented algorithms:
- `generate()`: Builds full state space as a graph
- `solution_dfs()`: Solves using Depth-First Search
- `solution_bfs()`: Solves using Breadth-First Search
- `best_first_search()`: Uses heuristic (number of items on goal side)

> Includes full state modeling, action simulation, and backtracking.

---

## 3. 🧩 Dots and Boxes - Minimax & MCTS

An implementation of the classic **Dots and Boxes** game featuring AI agents using:
- **Minimax with Alpha-Beta pruning**
- **Transposition Tables** to reduce visited states
- **Heuristic action sorting**
- **MCTS (Monte Carlo Tree Search)** with shared memory for improved performance

Key classes:
- `State`: Handles board state, actions, undoing moves
- `MinimaxAgent`: Uses heuristic evaluation and memoization
- `MCTSAgent`: Uses simulations with a shared tree

> Enhanced decision-making via action sorting and memory reuse significantly improves AI performance.

---

