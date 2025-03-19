import numpy as np

# Provided transform function and helper functions (from the previous turn)
def has_horizontal_blue_line(grid):
    """Checks if the grid has at least one horizontal line of blue pixels."""
    for row in grid:
        if all(pixel == 1 for pixel in row):
            return True
    return False

def has_vertical_gray_line(grid):
    """Checks if the grid has at least one vertical line of gray pixels."""
    for j in range(grid.shape[1]):
        if all(grid[:, j] == 5):
            return True
    return False

def transform(input_grid):
    # Check for existence of blue horizontal and gray vertical lines
    if has_horizontal_blue_line(input_grid) and has_vertical_gray_line(input_grid):
        # Create a 3x3 output grid filled with white (0)
        output_grid = np.zeros((3, 3), dtype=int)
        # Place a red (2) pixel at the center (1, 1)
        output_grid[1, 1] = 2
        return output_grid
    else:
        #  If conditions not met, could return original, or an empty grid, depends on task needs.
        #  Here we'll return original grid for cases lacking blue/grey, to clarify behavior
        return np.zeros((3,3), dtype=int) # Task specifies 3x3 grid

# The training examples (replace with actual data)
train_examples = [
    (np.array([[5, 5, 5, 5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5, 5, 5, 5],
               [1, 1, 1, 1, 1, 1, 1, 1, 1]]),
     np.array([[0, 0, 0],
               [0, 2, 0],
               [0, 0, 0]])),

    (np.array([[5, 5, 5, 5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5, 5, 5, 5],
               [1, 1, 1, 1, 1, 1, 1, 1, 1],
               [5, 5, 5, 5, 5, 5, 5, 5, 5]]),
     np.array([[0, 0, 0],
               [0, 2, 0],
               [0, 0, 0]])),

    (np.array([[5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5],
               [1, 1, 1, 1, 1, 1]]),
     np.array([[0, 0, 0],
               [0, 2, 0],
               [0, 0, 0]])),

    (np.array([[5, 5, 5, 5],
               [5, 5, 5, 5],
               [5, 5, 5, 5],
               [1, 1, 1, 1]]),
     np.array([[0, 0, 0],
               [0, 2, 0],
               [0, 0, 0]])),
    
     (np.array([[1, 1, 1],
               [5, 5, 5]]),
     np.array([[0, 0, 0],
               [0, 2, 0],
               [0, 0, 0]])),
]

# Evaluate each example
results = []
for input_grid, expected_output in train_examples:
    actual_output = transform(input_grid)
    success = np.array_equal(actual_output, expected_output)
    results.append((input_grid.tolist(), expected_output.tolist(), actual_output.tolist(), success))

for i, (input_grid, expected, actual, success) in enumerate(results):
    print(f"Example {i+1}:")
    print(f"  Input:\n{np.array(input_grid)}")
    print(f"  Expected Output:\n{np.array(expected)}")
    print(f"  Actual Output:\n{np.array(actual)}")
    print(f"  Success: {success}")
    print("-" * 20)