"""
Extracts a 3x3 subgrid from the input grid and transforms blue (4) and green (3) pixels to magenta (6).
The subgrid is a copy of a 3x3 region of the input grid.
"""

import numpy as np

def find_subgrid_start(input_grid):
    """
    Finds the top-left corner coordinates of the 3x3 subgrid to extract.
    Prioritizes regions with blue (4) and green (3) pixels.
    """
    rows, cols = input_grid.shape
    for r in range(rows - 2):
        for c in range(cols - 2):
            # Check if the 3x3 region exists
            if r + 3 <= rows and c + 3 <= cols:
                return (r, c) # Always returns the top-leftmost 3x3 area
    return (0, 0)  # Default in case no 3x3 region is found (shouldn't happen in ARC)

def transform(input_grid):
    """
    Transforms an input grid by extracting a 3x3 subgrid and replacing blue (4) and green (3) pixels with magenta (6).

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed output grid.
    """
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape

    # 1. Identify Source Subgrid
    start_row, start_col = find_subgrid_start(input_grid)

    # 2. Extract Subgrid
    output_grid = np.zeros((3, 3), dtype=int)
    for r in range(3):
        for c in range(3):
            output_grid[r, c] = input_grid[start_row + r, start_col + c]

    # 3. Color Transformation
    for r in range(3):
        for c in range(3):
            if output_grid[r, c] == 3 or output_grid[r, c] == 4:
                output_grid[r, c] = 6

    return output_grid