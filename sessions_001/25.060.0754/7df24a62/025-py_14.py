import numpy as np

def describe_grid(grid):
    rows, cols = grid.shape
    print(f"  Dimensions: {rows}x{cols}")
    unique_colors = np.unique(grid)
    print(f"  Unique Colors: {unique_colors}")
    for color in unique_colors:
        count = np.sum(grid == color)
        print(f"  Color {color}: Count = {count}")

def compare_grids(grid1, grid2):
    if grid1.shape != grid2.shape:
        print("  Grids have different dimensions.")
        return
    diff = grid1 != grid2
    diff_coords = np.argwhere(diff)
    num_diffs = diff_coords.shape[0]
    print(f"  Number of differences: {num_diffs}")
    if num_diffs > 0:
      print(f"  Difference coordinates and values:")
      for row, col in diff_coords:
          print(f"    ({row}, {col}): Expected {grid2[row, col]}, Actual {grid1[row, col]}")

examples = [
    (
        np.array([
            [4, 4, 4, 4, 4, 4, 0, 0, 0, 0],
            [4, 4, 4, 4, 4, 4, 0, 0, 0, 0],
            [4, 4, 4, 4, 4, 4, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 4, 4, 4, 4],
            [0, 0, 0, 0, 0, 0, 4, 1, 1, 4],
            [0, 0, 0, 0, 0, 0, 4, 1, 1, 4],
        ]),
        np.array([
            [1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 4, 4, 4, 4],
            [0, 0, 0, 0, 0, 0, 4, 1, 1, 4],
            [0, 0, 0, 0, 0, 0, 4, 1, 1, 4],
        ])
    ),
     (
        np.array([
            [4, 4, 4, 4, 4, 4, 0, 0, 0, 0],
            [4, 4, 4, 4, 4, 4, 0, 0, 0, 0],
            [4, 4, 4, 4, 4, 4, 0, 0, 0, 0],
            [0, 0, 0, 4, 4, 0, 0, 0, 0, 0],
            [0, 0, 0, 4, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 4, 4, 0, 0, 0, 0, 0],
        ]),
        np.array([
            [1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 4, 4, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
        ])
    ),
    (
        np.array([
            [4, 4, 4, 4, 4, 4, 0, 0, 0, 0],
            [4, 4, 4, 4, 4, 4, 0, 0, 0, 0],
            [4, 4, 4, 4, 4, 4, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 4, 4, 4, 4],
            [0, 0, 0, 0, 0, 0, 4, 1, 1, 4],
            [0, 0, 0, 0, 0, 0, 4, 4, 4, 4],
        ]),
        np.array([
            [1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 4, 4, 4, 4],
            [0, 0, 0, 0, 0, 0, 4, 1, 1, 4],
            [0, 0, 0, 0, 0, 0, 4, 1, 1, 4],
        ])
    ),
(
        np.array([
            [4, 4, 4, 4, 4, 4, 0, 0],
            [4, 4, 4, 4, 4, 4, 0, 0],
            [4, 4, 4, 4, 4, 4, 0, 0],
            [0, 0, 0, 4, 4, 0, 0, 0],
            [0, 0, 0, 1, 1, 0, 0, 0],
            [0, 0, 0, 1, 4, 0, 0, 0],
        ]),
        np.array([
            [1, 1, 1, 1, 1, 1, 0, 0],
            [1, 1, 1, 1, 1, 1, 0, 0],
            [1, 1, 1, 1, 1, 1, 0, 0],
            [0, 0, 0, 1, 1, 0, 0, 0],
            [0, 0, 0, 1, 1, 0, 0, 0],
            [0, 0, 0, 1, 1, 0, 0, 0],
        ])
    ),

]

for i, (input_grid, expected_output) in enumerate(examples):
    print(f"Example {i+1}:")
    print("Input Grid:")
    describe_grid(input_grid)
    print("Expected Output:")
    describe_grid(expected_output)
    actual_output = transform(input_grid)
    print("Actual Output:")
    describe_grid(actual_output)
    print("Comparison (Expected vs Actual):")
    compare_grids(actual_output, expected_output)
    print("-" * 40)