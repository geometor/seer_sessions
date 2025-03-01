import numpy as np

def find_lines(grid, color):
    lines = []
    rows, cols = grid.shape
    for r in range(rows):
      row_line = []
      for c in range(cols):
        if grid[r,c] == color:
          row_line.append((r,c))
      if row_line:
        lines.append(row_line)

    for c in range(cols):
      col_line = []
      for r in range(rows):
        if grid[r,c] == color:
          col_line.append((r,c))
      if col_line:
        lines.append(col_line)
    return lines

# Example Data (Replace with actual data from ARC tasks)
example_inputs = [
    np.array([
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 2, 2, 2, 1, 1, 1],
        [1, 4, 1, 2, 2, 2, 1, 1, 1],
        [1, 1, 1, 2, 2, 2, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 3, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1]
    ]),
    np.array([
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 2, 2, 2, 1, 1, 4, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ]),
    np.array([
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 4, 1, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ])
]

# Analyze each example
for i, input_grid in enumerate(example_inputs):
    green_lines = find_lines(input_grid, 3)
    print(f"Example {i+1} Green Lines:")
    print(green_lines)
