import heapq

INITIAL = ((1, 2, 3), (0, 4, 6), (7, 5, 8))
GOAL = ((1, 2, 3), (4, 5, 6), (7, 8, 0))


def h_manhattan_distance(state):
    goal_pos = {GOAL[r][c]: (r, c) for r in range(3) for c in range(3)}
    distance = 0

    for r in range(3):
        for c in range(3):
            val = state[r][c]
            if val != 0:
                gr, gc = goal_pos[val]
                distance += abs(r - gr) + abs(c - gc)

    return distance


def get_neighbors(state):
    br, bc = 0, 0
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
    h0 = h_manhattan_distance(INITIAL)
    count = 0
    open_list = [(h0, 0, count, INITIAL, [INITIAL])]
    visited = set()

    while open_list:
        f, g, _, current, path = heapq.heappop(open_list)

        if current == GOAL:
            return path, g

        if current in visited:
            continue
        visited.add(current)

        for next_state in get_neighbors(current):
            if next_state not in visited:
                g_new = g + 1
                h_new = h_manhattan_distance(next_state)
                f_new = g_new + h_new
                count += 1
                heapq.heappush(
                    open_list,
                    (f_new, g_new, count, next_state, path + [next_state]),
                )

    return None, 0


if __name__ == "__main__":
    path, depth = a_star()

    print("MANHATTAN DISTANCE HEURISTIC")

    if path:
        print(f"Total Steps / Depth (g): {depth}\n")
        for step, state in enumerate(path):
            print(f"Step {step}:")
            for row in state:
                print(" ", list(row))
            print()
    else:
        print("No solution found.")