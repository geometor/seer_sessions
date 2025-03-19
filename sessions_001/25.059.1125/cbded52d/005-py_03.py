import numpy as np

# Example data (replace with actual data from the task)
# Input and output pairs
train_pairs = [
    (np.array([[0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 1, 4, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 1, 4, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0]]),
     np.array([[0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 4, 4, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 4, 4, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0]])),

      (np.array([[0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 1, 2, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 1, 2, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0]]),
     np.array([[0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 2, 2, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 2, 2, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0]])),

      (np.array([[0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 1, 4, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 1, 2, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 1, 2, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0]]),
     np.array([[0, 0, 0, 4, 4, 0, 0, 0],
       [0, 0, 0, 4, 4, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 2, 2, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 2, 2, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0]]))
]

def analyze_changes(input_grid, output_grid):
    """Analyzes the differences between input and output grids."""
    changes = []
    for i in range(input_grid.shape[0]):
        for j in range(input_grid.shape[1]):
            if input_grid[i, j] != output_grid[i, j]:
                changes.append({
                    "row": i,
                    "col": j,
                    "old_color": input_grid[i, j],
                    "new_color": output_grid[i, j]
                })
    return changes

# Analyze each pair and store results
results = []
for i, (input_grid, output_grid) in enumerate(train_pairs):
    changes = analyze_changes(input_grid, output_grid)
    results.append({
        "pair_index": i,
        "changes": changes
    })

# Print results for review
for result in results:
    print(f"Pair {result['pair_index']}:")
    if result['changes']:
        for change in result['changes']:
            print(f"  Row: {change['row']}, Col: {change['col']}, Old Color: {change['old_color']}, New Color: {change['new_color']}")
    else:
        print("  No changes found.")
    print("-" * 20)

# Example of accessing data for pair 0, change 1:
# print(results[0]['changes'][0]['old_color'])