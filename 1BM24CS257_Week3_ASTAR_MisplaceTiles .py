import heapq

INITIAL =  ((1, 2, 3), (4, 0, 6), (7, 5, 8))
GOAL = ((1, 2, 3), (4, 5, 6), (7, 8, 0))


def h_misplaced_tiles(state):
    """Calculates h(n): Number of misplaced non-blank tiles."""
    count = 0
    for r in range(3):
        for c in range(3):
            if state[r][c] != 0 and state[r][c] != GOAL[r][c]:
                count += 1
    return count


def get_neighbors(state):
    """Generates next valid puzzle configurations."""
    for r in range(3):
        for c in range(3):
            if state[r][c] == 0:
                br, bc = r, c

    neighbors = []
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)] 
    for dr, dc in moves:
        nr, nc = br + dr, bc + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            board = [list(row) for row in state]
            board[br][bc], board[nr][nc] = board[nr][nc], board[br][bc]
            neighbors.append(tuple(tuple(row) for row in board))

    return neighbors


def a_star():
    """Solves 8-Puzzle using Misplaced Tiles Heuristic."""
    h0 = h_misplaced_tiles(INITIAL)
    open_list = [(h0, 0, INITIAL, [INITIAL])]
    visited = set()

    while open_list:
        f, g, current, path = heapq.heappop(open_list)

        if current == GOAL:
            return path, g

        if current in visited:
            continue
        visited.add(current)

        for next_state in get_neighbors(current):
            if next_state not in visited:
                g_new = g + 1
                h_new = h_misplaced_tiles(next_state)
                f_new = g_new + h_new
                heapq.heappush(
                    open_list, (f_new, g_new, next_state, path + [next_state])
                )

    return None, 0


if __name__ == "__main__":
    path, depth = a_star()

    print("MISPLACED TILES HEURISTIC")
    print(f"Total Steps / Depth (g): {depth}\n")

    for step, state in enumerate(path):
        print(f"Step {step}:")
        for row in state:
            print(" ", list(row))
        print()