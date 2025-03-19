import numpy as np

def find_square(grid, color, size=2):
    """Finds a square of a given color and size."""
    rows, cols = grid.shape
    for r in range(rows - size + 1):
        for c in range(cols - size + 1):
            if np.all(grid[r:r+size, c:c+size] == color):
                return r, c
    return None, None

def transform(input_grid):
    # Initialize output_grid as a zero-filled array of the same size/shape as input
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Find the blue square.
    blue_row, _ = find_square(input_grid, 1)
    if blue_row is not None:
        # Place blue pixels diagonally.
        for i in range(4):
            output_grid[blue_row + i, i] = 1

    # Find the red square.
    red_row, red_col = find_square(input_grid, 2)
    if red_row is not None:
        # Place red square in the last two columns.
        output_grid[red_row, cols-2:cols] = 2
        output_grid[red_row + 1, cols-2:cols] = 2
        # additional red pixels based on the original red square location
        output_grid[red_row + 3, cols -1] = 2
        output_grid[red_row + 4, cols -1] = 2

    return output_grid

task = "6e82a1ae"
examples = [
  {"input": [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 1, 0, 0, 0, 0, 0], [0, 1, 1, 0, 0, 2, 2, 0], [0, 0, 0, 0, 0, 2, 2, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]], "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 2, 2, 0], [0, 1, 0, 0, 0, 0, 0, 2, 2, 0], [0, 0, 1, 0, 0, 0, 0, 0, 0, 2], [0, 0, 0, 1, 0, 0, 0, 0, 0, 2], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]},
  {"input": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 1, 0, 0, 0, 0, 0, 0], [0, 1, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 2, 2, 0, 0], [0, 0, 0, 0, 0, 2, 2, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]], "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 2, 2, 0, 0], [0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0]]},
  {"input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 1, 0, 0, 0, 0, 0, 0, 0], [0, 1, 1, 0, 0, 2, 2, 0, 0, 0], [0, 0, 0, 0, 0, 2, 2, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 2, 2, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0, 2, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]}
]

def compare_grids(grid1, grid2):
    return np.array_equal(grid1, grid2)

results = []
for example in examples:
  input_grid = np.array(example['input'])
  expected_output = np.array(example['output'])
  predicted_output = transform(input_grid)
  results.append(compare_grids(predicted_output, expected_output))
  print(f"Example: {example['input']} \nExpected: {example['output']} \nPredicted: {predicted_output.tolist()} \nEqual: {compare_grids(predicted_output, expected_output)}\n")

print(f"Overall Results: {results}")