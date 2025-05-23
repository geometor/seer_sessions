import numpy as np

"""
This transformation operates on a grid by identifying a pattern on the left, filling the area to the right based on the first column's color, and appending the last two columns of the pattern to the right edge.

1.  Initialize the output grid as a copy of the input grid.
2.  Determine the width of the non-white pattern at the left edge of the input grid (`pattern_width`). This is the index of the first column where all pixels are white (0). If no such column exists, `pattern_width` is the total grid width.
3.  Iterate through each row `r` of the grid:
    a. Get the `fill_color` from the pixel in the first column (index 0) of the input grid's current row (`input_grid[r, 0]`).
    b. Identify the columns to be filled in the current row of the output grid: start from column index `pattern_width` and go up to, but not including, the second-to-last column index (`width - 2`).
    c. If the starting column index is less than the ending column index, fill these columns in the output grid with the `fill_color`.
4.  Check if the pattern has at least two columns (`pattern_width >= 2`) and if the grid width allows space for the first appended column (`width >= 2`). If both true, copy the second-to-last column of the input pattern (column index `pattern_width - 2`) to the second-to-last column of the output grid (column index `width - 2`).
5.  Check if the pattern has at least one column (`pattern_width >= 1`) and if the grid width allows space for the second appended column (`width >= 1`). If both true, copy the last column of the input pattern (column index `pattern_width - 1`) to the last column of the output grid (column index `width - 1`).
6.  Return the modified output grid.
"""

def find_pattern_width(grid):
    """
    Finds the width of the non-white pattern starting from the left edge.
    The pattern ends at the first column that consists entirely of white (0) pixels.

    Args:
        grid: A numpy array representing the grid.

    Returns:
        An integer representing the width of the pattern (index of the first all-white column).
    """
    height, width = grid.shape
    for c in range(width):
        # Check if all pixels in the current column are white (0)
        if np.all(grid[:, c] == 0):
            return c  # Return the index of the first all-white column
    return width  # If no all-white column is found, the pattern spans the entire width

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Convert the input list of lists to a numpy array for efficient manipulation
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # 1. Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_np)

    # 2. Determine the width of the initial colored pattern
    pattern_width = find_pattern_width(input_np)

    # 3. Fill the area to the right of the pattern (up to the last two columns)
    # Iterate through each row
    for r in range(height):
        # 3a. Get the fill color from the first column of the current row in the input
        fill_color = input_np[r, 0]

        # 3b. Define the columns to fill in the output grid
        fill_start_col = pattern_width
        fill_end_col = width - 2 # Exclusive index

        # 3c. Fill the specified columns if the range is valid
        if fill_start_col < fill_end_col:
             output_grid[r, fill_start_col:fill_end_col] = fill_color

    # 4. Append the second-to-last column of the pattern if possible
    # Check if pattern is wide enough and grid has space for the destination column
    if pattern_width >= 2 and width >= 2:
        source_col_idx = pattern_width - 2
        dest_col_idx = width - 2
        output_grid[:, dest_col_idx] = input_np[:, source_col_idx]

    # 5. Append the last column of the pattern if possible
    # Check if pattern is wide enough and grid has space for the destination column
    if pattern_width >= 1 and width >= 1:
        source_col_idx = pattern_width - 1
        dest_col_idx = width - 1
        output_grid[:, dest_col_idx] = input_np[:, source_col_idx]

    # 6. Convert the resulting numpy array back to a list of lists before returning
    return output_grid.tolist()