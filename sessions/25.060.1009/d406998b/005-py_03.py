import numpy as np

def get_adjacent_pixels(grid, row, col):
    """Gets the values of the adjacent pixels, handling edge cases."""
    rows, cols = grid.shape
    adjacent = []
    for i in range(max(0, row - 1), min(rows, row + 2)):
        for j in range(max(0, col - 1), min(cols, col + 2)):
            if (i, j) != (row, col):  # Exclude the pixel itself
                adjacent.append(grid[i, j])
    return adjacent

def get_hv_adjacent_pixels(grid, row, col):
    """Gets values of horizontally/vertically adjacent pixels."""
    rows, cols = grid.shape
    adjacent = []
    if row > 0:
        adjacent.append(grid[row-1, col]) # Up
    if row < rows - 1:
        adjacent.append(grid[row+1, col]) # Down
    if col > 0:
        adjacent.append(grid[row, col-1]) # Left
    if col < cols - 1:
        adjacent.append(grid[row, col+1]) # Right
    return adjacent

def analyze_example(input_grid, output_grid):
    """Analyzes changes and adjacency for a single example."""
    changed_pixels = []
    rows, cols = input_grid.shape
    for row in range(rows):
        for col in range(cols):
            if input_grid[row, col] != output_grid[row, col]:
                changed_pixels.append((row, col, input_grid[row, col], output_grid[row, col]))

    print("Changed Pixels:")
    for row, col, old_val, new_val in changed_pixels:
        adjacent = get_adjacent_pixels(input_grid, row, col)
        hv_adjacent = get_hv_adjacent_pixels(input_grid, row, col)
        gray_count = adjacent.count(5)
        white_count = adjacent.count(0)
        hv_gray_count = hv_adjacent.count(5)
        hv_white_count = hv_adjacent.count(0)

        print(f"  ({row}, {col}): {old_val} -> {new_val}")
        print(f"    Adjacent: Gray={gray_count}, White={white_count}, Other={len(adjacent) - gray_count - white_count}")
        print(f"    HV Adjacent: Gray={hv_gray_count}, White={hv_white_count}, Other={len(hv_adjacent) - hv_gray_count- hv_white_count}")
    print("Unchanged Gray Pixels adjacent to Gray and White")
    for row in range(rows):
      for col in range(cols):
        if input_grid[row, col] == 5 and output_grid[row,col] == 5:
          adjacent = get_adjacent_pixels(input_grid, row, col)
          hv_adjacent = get_hv_adjacent_pixels(input_grid, row, col)
          gray_count = adjacent.count(5)
          white_count = adjacent.count(0)
          hv_gray_count = hv_adjacent.count(5)
          hv_white_count = hv_adjacent.count(0)
          if gray_count > 0 and white_count > 0:
            print(f"  ({row}, {col}): {input_grid[row,col]}")
            print(f"    Adjacent: Gray={gray_count}, White={white_count}, Other={len(adjacent) - gray_count - white_count}")
            print(f"    HV Adjacent: Gray={hv_gray_count}, White={hv_white_count}, Other={len(hv_adjacent) - hv_gray_count- hv_white_count}")
# Example data (replace with actual task data)
# 93b581b8
task_id = "93b581b8"

example_inputs = [
  np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 5, 5, 5, 0, 0, 0, 0],
            [0, 0, 0, 5, 0, 5, 0, 0, 0, 0],
            [0, 0, 0, 5, 5, 5, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
  np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 5, 5, 5, 5, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 5, 0, 0, 5, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 5, 5, 5, 5, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
    np.array([[5, 0, 5, 0, 5],
              [0, 5, 0, 5, 0],
              [5, 0, 5, 0, 5],
              [0, 5, 0, 5, 0]]),
]
example_outputs = [
  np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 5, 3, 5, 0, 0, 0, 0],
            [0, 0, 0, 5, 0, 5, 0, 0, 0, 0],
            [0, 0, 0, 5, 3, 5, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
  np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 5, 3, 3, 5, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 5, 0, 0, 5, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 5, 3, 3, 5, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
    np.array([[5, 0, 5, 0, 5],
              [0, 3, 0, 3, 0],
              [5, 0, 5, 0, 5],
              [0, 3, 0, 3, 0]]),
]

for i in range(len(example_inputs)):
    print(f"Example {i+1}:")
    analyze_example(example_inputs[i], example_outputs[i])
    print("-" * 20)