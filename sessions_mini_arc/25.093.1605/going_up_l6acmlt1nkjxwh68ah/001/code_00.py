"""
Transformation Rule:
1. Identify all rows in the input grid that contain at least one non-zero element ("pattern rows"). Maintain their original relative order.
2. If no pattern rows exist, return a grid of zeros with the same dimensions as the input.
3. Otherwise, create a new output grid with the same dimensions as the input.
4. Place the identified pattern rows sequentially into the output grid, starting from the top row.
5. If the number of pattern rows is less than the total height of the grid, fill the remaining rows of the output grid by repeating the *last* identified pattern row.
"""

import numpy as np

def find_pattern_rows(grid):
    """
    Identifies rows containing non-zero elements.
    
    Args:
        grid (np.ndarray): The input grid.

    Returns:
        list: A list of rows (as np.ndarrays) that contain non-zero elements,
              preserving their original relative order.
    """
    pattern_rows = []
    for row in grid:
        if np.any(row != 0):  # Check if any element in the row is non-zero
            pattern_rows.append(row)
    return pattern_rows

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list of lists or np.ndarray): The input grid.

    Returns:
        np.ndarray: The transformed output grid.
    """
    # Convert input to numpy array for easier manipulation
    input_array = np.array(input_grid)
    grid_height, grid_width = input_array.shape

    # 1. Identify Pattern Rows
    pattern_rows = find_pattern_rows(input_array)

    # 2. Handle Empty Case
    if not pattern_rows:
        # If no pattern rows found, return a grid of zeros
        return np.zeros_like(input_array)

    # 3. Determine Last Pattern Row
    last_pattern_row = pattern_rows[-1]
    num_pattern_rows = len(pattern_rows)

    # 4. Construct Output Grid (initialize with zeros)
    output_grid = np.zeros_like(input_array)

    # 5. Fill with Pattern Rows
    # Copy the identified pattern rows into the top of the output grid
    rows_to_copy = min(num_pattern_rows, grid_height) # Ensure we don't exceed output height
    output_grid[:rows_to_copy, :] = np.array(pattern_rows[:rows_to_copy])

    # 6. Fill Remaining Rows
    # If pattern rows don't fill the grid, repeat the last pattern row
    if num_pattern_rows < grid_height:
        for i in range(num_pattern_rows, grid_height):
            output_grid[i, :] = last_pattern_row

    # 7. Return the constructed output grid
    return output_grid
