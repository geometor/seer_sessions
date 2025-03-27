"""
Fill the gap between two boundary pixels in a row, using their respective colors and placing a gray separator in the middle.

1. Identify the target row: Find the row containing exactly two non-white pixels, located at the first (column 0) and last (column width - 1) columns, with all intermediate columns being white (0).
2. If no such row exists, return the input grid unchanged.
3. If the target row is found:
    a. Get the color of the leftmost pixel (color_left) and the rightmost pixel (color_right).
    b. Calculate the middle column index: middle_column = (width - 1) // 2.
    c. In the target row of the output grid:
        i. Fill pixels from column 1 up to (but not including) middle_column with color_left.
        ii. Set the pixel at middle_column to gray (5).
        iii. Fill pixels from middle_column + 1 up to (but not including) width - 1 with color_right.
4. Return the modified grid.
"""

import numpy as np

def _find_target_row(grid):
    """
    Finds the index of the row matching the target criteria.

    Args:
        grid (np.array): The input grid.

    Returns:
        int or None: The index of the target row, or None if no such row is found.
    """
    height, width = grid.shape
    if width < 2: # Need at least two columns for boundary pixels
        return None

    for r in range(height):
        row = grid[r, :]
        # Check boundary pixels are non-white
        if row[0] != 0 and row[-1] != 0:
            # Check if all intermediate pixels are white
            is_target = True
            if width > 2: # Only check intermediate if they exist
                 for c in range(1, width - 1):
                     if row[c] != 0:
                         is_target = False
                         break
            if is_target:
                return r # Found the target row
    return None # No target row found

def transform(input_grid):
    """
    Transforms the input grid according to the specified rule.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_np)

    # Find the target row
    target_row_index = _find_target_row(input_np)

    # If a target row is found, apply the transformation
    if target_row_index is not None:
        # Get boundary colors
        color_left = input_np[target_row_index, 0]
        color_right = input_np[target_row_index, width - 1]

        # Calculate middle column index
        # Note: Using integer division `//` correctly handles both even and odd widths.
        # For width=11, middle is (11-1)//2 = 5.
        # For width=10, middle is (10-1)//2 = 4.
        middle_column = (width - 1) // 2

        # Fill the left segment (if space exists)
        # Range is [1, middle_column)
        for c in range(1, middle_column):
            output_grid[target_row_index, c] = color_left

        # Place the gray separator (only if width > 1)
        if width > 1:
             output_grid[target_row_index, middle_column] = 5 # Gray color

        # Fill the right segment (if space exists)
        # Range is [middle_column + 1, width - 1)
        for c in range(middle_column + 1, width - 1):
            output_grid[target_row_index, c] = color_right

    # Convert back to list of lists for the expected output format
    return output_grid.tolist()