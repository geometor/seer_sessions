import numpy as np

def get_quadrant_color(grid, quadrant):
    """
    Identifies a non-white color within a specified quadrant of the grid.

    Args:
        grid: The input numpy array.
        quadrant: A tuple (row_start, row_end, col_start, col_end) defining the quadrant.

    Returns:
        A non-white color (integer) found in the quadrant, or None if only white is present.
    """
    row_start, row_end, col_start, col_end = quadrant
    subgrid = grid[row_start:row_end, col_start:col_end]
    unique_colors = np.unique(subgrid)
    for color in unique_colors:
        if color != 0:  # Exclude white (0)
            return color
    return None 

def transform(input_grid):
    """
    Transforms the input grid into a 2x2 output grid.  The output grid represents colors of 4
    quadrants of the input.
    """
    # Initialize output_grid
    rows, cols = input_grid.shape
    output_grid = np.zeros((2, 2), dtype=int)

    # Define quadrants
    mid_row = rows // 2
    mid_col = cols // 2
    quadrants = {
        "top_left": (0, mid_row, 0, mid_col),
        "top_right": (0, mid_row, mid_col, cols),
        "bottom_left": (mid_row, rows, 0, mid_col),
        "bottom_right": (mid_row, rows, mid_col, cols),
    }

    # Change output pixels based on quadrant colors
    output_grid[0, 0] = get_quadrant_color(input_grid, quadrants["top_left"])
    output_grid[0, 1] = get_quadrant_color(input_grid, quadrants["top_right"])
    output_grid[1, 0] = get_quadrant_color(input_grid, quadrants["bottom_left"])
    output_grid[1, 1] = get_quadrant_color(input_grid, quadrants["bottom_right"])

    return output_grid

# Provided training examples and expected outputs
train_examples = [
    (np.array([[0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 3],
               [0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0]]), np.array([[0, 0], [0, 3]])),
    (np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 5, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0]]), np.array([[0, 0], [5, 0]])),
    (np.array([[0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0],
               [0, 0, 7, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 6, 0]]), np.array([[7, 0], [0, 6]])),
    (np.array([[0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 5, 0, 2, 0, 0]]), np.array([[0, 0], [5, 2]])),
  (np.array([[0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 2]]), np.array([[1, 0],
                                                   [0, 2]]))
]

print("Execution Results:")
for i, (input_grid, expected_output) in enumerate(train_examples):
    actual_output = transform(input_grid)
    print(f"Example {i + 1}:")
    print(f"  Input:\n{input_grid}")
    print(f"  Expected Output:\n{expected_output}")
    print(f"  Actual Output:\n{actual_output}")
    print(f"  Match: {np.array_equal(actual_output, expected_output)}")
    print("-" * 20)