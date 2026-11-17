"""
N-Queens Puzzle Solver using Hill Climbing (steepest-ascent with random restarts)
Mini Project - Artificial Intelligence

State   : list where state[col] = row of the queen in that column (one queen per column)
Cost    : number of pairs of queens attacking each other (goal = 0)
Move    : move one queen to another row inside its own column
"""
import random
import time


def cost(state):
    """Count pairs of queens that attack each other (same row or same diagonal)."""
    n = len(state)
    attacks = 0
    for i in range(n):
        for j in range(i + 1, n):
            if state[i] == state[j] or abs(state[i] - state[j]) == j - i:
                attacks += 1
    return attacks


def best_neighbour(state):
    """Try every single-queen move; return the neighbour with the lowest cost."""
    n = len(state)
    best_cost = cost(state)
    best_states = []
    for col in range(n):
        original = state[col]
        for row in range(n):
            if row == original:
                continue
            state[col] = row
            c = cost(state)
            if c < best_cost:
                best_cost, best_states = c, [(col, row)]
            elif c == best_cost and best_states:
                best_states.append((col, row))
        state[col] = original
    if not best_states:
        return None, best_cost
    col, row = random.choice(best_states)
    new_state = state[:]
    new_state[col] = row
    return new_state, best_cost


def hill_climb(n, max_steps=1000):
    """One run of steepest-ascent hill climbing from a random start."""
    state = [random.randrange(n) for _ in range(n)]
    history = [cost(state)]
    for _ in range(max_steps):
        if history[-1] == 0:
            break
        new_state, new_cost = best_neighbour(state)
        if new_state is None:          # stuck: local maximum / plateau / shoulder
            break
        state = new_state
        history.append(new_cost)
    return state, history


def solve(n, max_restarts=1000):
    """Random-restart hill climbing: restart until a solution is found."""
    restarts = 0
    total_steps = 0
    while restarts < max_restarts:
        state, history = hill_climb(n)
        total_steps += len(history) - 1
        if history[-1] == 0:
            return state, restarts, total_steps, history
        restarts += 1
    return None, restarts, total_steps, history


def print_board(state):
    n = len(state)
    for row in range(n):
        print(" ".join("Q" if state[col] == row else "." for col in range(n)))


if __name__ == "__main__":
    try:
        n = int(input("Enter the value of N (N >= 4): "))
    except ValueError:
        print("Invalid input: please enter a whole number.")
        raise SystemExit
    if n in (2, 3) or n < 1:
        print(f"No solution exists for N = {n}.")
    else:
        start = time.time()
        sol, restarts, steps, _ = solve(n)
        print(f"Solved with {restarts} restart(s) and {steps} total moves in {time.time()-start:.4f} s")
        print("Solution (column -> row):", sol)
        print_board(sol)
