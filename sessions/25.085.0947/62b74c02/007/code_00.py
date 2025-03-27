import numpy as np

"""
Transforms the input grid by identifying an initial pattern on the left, potentially filling a central area based on the first column's colors, and appending a copy of the initial pattern to the right edge.

1.  Identify the 'initial pattern': Find the columns from the left edge (column 0) up to the first column consisting entirely of white pixels (0). The number of columns in this pattern is `pattern_width`.
2.  Initialize the output grid as a copy of the input grid.
3.  Determine the boundaries:
    - Fill area starts at column `pattern_width`.
    - Append area starts at column `width - pattern_width`.
    - Fill area ends just before the append area starts (exclusive index `width - pattern_width`).
4.  Fill the central area (if it exists, i.e., if `width > 2 * pattern_width`): For each row, fill the columns from `pattern_width` up to (but not including) `width - pattern_width` with the color found in the first column (index 0) of that row in the input grid.
5.  Append the pattern copy (if `pattern_width > 0`): Copy the columns of the initial pattern (input columns 0 to `pattern_width - 1`) to the end of the output grid (output columns `width - pattern_width` to `width - 1`).
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
    # Convert input to numpy array
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # 1. Identify Pattern Width
    pattern_width = find_pattern_width(input_np)

    # 2. Initialize Output Grid
    output_grid = np.copy(input_np)

    # 3. Calculate Boundaries
    fill_start_col = pattern_width
    # The fill area ends just before the appended pattern starts
    fill_end_col = width - pattern_width # Exclusive index
    append_start_col = width - pattern_width
    append_end_col = width # Exclusive index

    # 4. Fill Area (if applicable)
    # Check if there's space for a fill area between the initial pattern and the appended pattern
    if fill_start_col < fill_end_col: # Equivalent to width > 2 * pattern_width
        for r in range(height):
            # Get the fill color from the first column of the input grid for this row
            fill_color = input_np[r, 0]
            # Apply the fill color to the designated columns in the output grid for this row
            output_grid[r, fill_start_col:fill_end_col] = fill_color

    # 5. Append Pattern (if applicable)
    # Check if there is a pattern to append (pattern_width > 0)
    # Also ensure the append columns are within the grid bounds (implicitly true if pattern_width <= width)
    if pattern_width > 0:
         # Check if the calculated append indices are valid (should always be if pattern_width determined correctly)
         if append_start_col < width:
            # Copy the initial pattern columns from input to the append area in output
            # Source: input_np columns 0 to pattern_width-1
            # Destination: output_grid columns append_start_col to append_end_col-1
            output_grid[:, append_start_col:append_end_col] = input_np[:, 0:pattern_width]


    # Convert the resulting numpy array back to a list of lists before returning
    return output_grid.tolist()