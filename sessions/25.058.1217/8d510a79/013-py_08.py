import numpy as np

def find_gray_line(grid):
    """Finds the row index of a horizontal gray line, if it exists."""
    for i, row in enumerate(grid):
        if np.all(row == 5):
            return i
    return -1  # Return -1 if no gray line is found

def transform(input_grid):
    """Transforms the input grid according to the rules."""
    output_grid = np.copy(input_grid)
    gray_line_row = find_gray_line(input_grid)

    if gray_line_row != -1:
        # Perform vertical reflection
        for j in range(input_grid.shape[1]):
            for i in range(gray_line_row - 1, -1, -1):
                output_grid[gray_line_row - (gray_line_row - i), j] = input_grid[i, j]
            for i in range(gray_line_row + 1, input_grid.shape[0]):
                output_grid[gray_line_row + (i - gray_line_row), j] = input_grid[i, j]
    else:
        # Output is identical to input
        pass # output_grid is already a copy of input_grid

    return output_grid

def compare_grids(grid1, grid2):
    return np.array_equal(grid1, grid2)

train_input_output_pairs = [
([
    np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 5, 5, 5, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
    np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 5, 5, 5, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0]])
    ], "Example 1"),
([
    np.array([[8, 8, 8, 8, 8, 8, 8, 8],
              [8, 8, 8, 8, 8, 8, 8, 8],
              [8, 8, 8, 8, 8, 8, 8, 8],
              [5, 5, 5, 5, 5, 5, 5, 5],
              [8, 8, 8, 8, 8, 8, 8, 8],
              [8, 8, 8, 8, 8, 8, 8, 8],
              [8, 8, 8, 8, 8, 8, 8, 8]]),
    np.array([[8, 8, 8, 8, 8, 8, 8, 8],
              [8, 8, 8, 8, 8, 8, 8, 8],
              [8, 8, 8, 8, 8, 8, 8, 8],
              [5, 5, 5, 5, 5, 5, 5, 5],
              [8, 8, 8, 8, 8, 8, 8, 8],
              [8, 8, 8, 8, 8, 8, 8, 8],
              [8, 8, 8, 8, 8, 8, 8, 8]])
    ], "Example 2"),
([
    np.array([[5, 5, 5, 5, 5]]),
    np.array([[5, 5, 5, 5, 5]])
    ], "Example 3"),
([
    np.array([[1, 1, 1, 1, 1, 1, 1, 1, 1],
              [1, 2, 3, 4, 5, 6, 7, 8, 9],
              [5, 5, 5, 5, 5, 5, 5, 5, 5],
              [9, 8, 7, 6, 5, 4, 3, 2, 1],
              [4, 4, 4, 4, 4, 4, 4, 4, 4]]),
    np.array([[1, 1, 1, 1, 1, 1, 1, 1, 1],
              [1, 2, 3, 4, 5, 6, 7, 8, 9],
              [5, 5, 5, 5, 5, 5, 5, 5, 5],
              [9, 8, 7, 6, 5, 4, 3, 2, 1],
              [4, 4, 4, 4, 4, 4, 4, 4, 4]])
    ], "Example 4"),
([
    np.array([[1, 1, 1],
              [2, 2, 2],
              [3, 3, 3],
              [4, 4, 4],
              [5, 5, 5],
              [6, 6, 6],
              [7, 7, 7],
              [8, 8, 8],
              [9, 9, 9]]),
    np.array([[1, 1, 1],
              [2, 2, 2],
              [3, 3, 3],
              [4, 4, 4],
              [5, 5, 5],
              [6, 6, 6],
              [7, 7, 7],
              [8, 8, 8],
              [9, 9, 9]])
    ], "Example 5")
]

for (input_grid, expected_output), example_name in train_input_output_pairs:
    transformed_grid = transform(input_grid)
    gray_line_row = find_gray_line(input_grid)
    is_correct = compare_grids(transformed_grid, expected_output)
    print(f"{example_name}:")
    print(f"  Gray Line Row: {gray_line_row}")
    print(f"  Is Correct: {is_correct}")
    print(f"  Transformed Grid:\n{transformed_grid}")
    print(f"  Expected Output:\n{expected_output}")
    print("-" * 20)