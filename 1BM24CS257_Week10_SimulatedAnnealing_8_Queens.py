import math
import random


def calculate_cost(state):
  """Calculate number of attacking pairs of queens."""
  cost = 0
  n = len(state)
  for i in range(n):
    for j in range(i + 1, n):
      # Check same row or same diagonal
      if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
        cost += 1
  return cost


def get_random_neighbor(state):
  """Move one random queen to a different random row in its column."""
  neighbor = list(state)
  col = random.randint(0, len(state) - 1)
  new_row = random.randint(0, len(state) - 1)
  while new_row == neighbor[col]:
    new_row = random.randint(0, len(state) - 1)
  neighbor[col] = new_row
  return neighbor


def simulated_annealing(initial_temp=100.0, cooling_rate=0.995, min_temp=1e-4):
  # 1. Initialize random state (one queen per column)
  current = [random.randint(0, 7) for _ in range(8)]
  current_cost = calculate_cost(current)
  T = initial_temp
  steps = 0

  # 3. Loop while T > min_temp (approximating T > 0) and solution not yet found
  while T > min_temp and current_cost > 0:
    # 4. Pick random neighbor
    next_state = get_random_neighbor(current)
    next_cost = calculate_cost(next_state)

    # 5. Compute change in energy (cost)
    delta_e = current_cost - next_cost

    # 6-10. Accept better state or worse state with probability e^(ΔE / T)
    if delta_e > 0 or random.random() < math.exp(delta_e / T):
      current = next_state
      current_cost = next_cost

    # 11. Decrease temperature
    T *= cooling_rate
    steps += 1

  return current, current_cost, steps


def print_board(state):
  for row in range(8):
    line = ""
    for col in range(8):
      line += "Q " if state[col] == row else ". "
    print(line)


# Run solver
random.seed(42)
solution, final_cost, total_steps = simulated_annealing()

print(f"Final State (Row positions per column): {solution}")
print(f"Attacking Pairs (Cost): {final_cost}")
print(f"Steps Taken: {total_steps}\n")
print("8-Queens Board Configuration:")
print_board(solution)