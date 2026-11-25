import math


def alpha_beta(depth, node_index, is_max, values, alpha, beta, max_depth, path):
  # Base case: leaf node reached
  if depth == max_depth:
    return values[node_index], path + [values[node_index]]

  if is_max:
    best = -math.inf
    best_path = []
    # Each node has 2 children in this binary game tree
    for i in range(2):
      child_idx = node_index * 2 + i
      val, current_path = alpha_beta(
          depth + 1,
          child_idx,
          False,
          values,
          alpha,
          beta,
          max_depth,
          path + [f"MAX(d={depth})"],
      )
      if val > best:
        best = val
        best_path = current_path

      alpha = max(alpha, best)

      # Beta Cutoff
      if beta <= alpha:
        pruned_idx = node_index * 2 + (i + 1)
        if i + 1 < 2:
          print(
              f"Pruned at depth {depth+1} (child index {pruned_idx}) because"
              f" beta ({beta}) <= alpha ({alpha})"
          )
        break
    return best, best_path

  else:
    best = math.inf
    best_path = []
    for i in range(2):
      child_idx = node_index * 2 + i
      val, current_path = alpha_beta(
          depth + 1,
          child_idx,
          True,
          values,
          alpha,
          beta,
          max_depth,
          path + [f"MIN(d={depth})"],
      )
      if val < best:
        best = val
        best_path = current_path

      beta = min(beta, best)

      # Alpha Cutoff
      if beta <= alpha:
        pruned_idx = node_index * 2 + (i + 1)
        if i + 1 < 2:
          print(
              f"Pruned at depth {depth+1} (child index {pruned_idx}) because"
              f" beta ({beta}) <= alpha ({alpha})"
          )
        break
    return best, best_path


# Leaf values from the lab observation problem
leaf_values = [10, 9, 14, 18, 5, 4, 50, 3]
tree_depth = int(math.log2(len(leaf_values)))

optimal_value, optimal_path = alpha_beta(
    0, 0, True, leaf_values, -math.inf, math.inf, tree_depth, []
)

print("\nOptimal Root Value:", optimal_value)
print("Optimal Path:", " -> ".join(map(str, optimal_path)))