"""
Identifies a 7x7 "flower" pattern within the input grid and returns the 7x7 region. The flower is identified by having a non-black center.
"""

import numpy as np

def get_potential_flower(grid, center_row, center_col):
    """Extracts the 7x7 grid centered at the given coordinates."""
    rows, cols = grid.shape
    if not (3 <= center_row < rows - 3 and 3 <= center_col < cols - 3):
        return None  # Center too close to edge for 7x7

    return grid[center_row-3:center_row+4, center_col-3:center_col+4]


def find_flower_center(grid):
    """Finds the center coordinates (row, col) of a potential flower pattern."""
    rows, cols = grid.shape
    for row in range(rows):
        for col in range(cols):
            if grid[row, col] != 0:  # Non-black center
                # Check if a full 7x7 can be extracted
                if 3 <= row < rows - 3 and 3 <= col < cols - 3:
                    return row, col
    return None, None  # No flower center found

def transform(input_grid):
    input_grid = np.array(input_grid)
    
    # Find a potential flower's center
    center_row, center_col = find_flower_center(input_grid)

    if center_row is None:
        return None

    # Extract the 7x7 region around the center
    flower_grid = get_potential_flower(input_grid, center_row, center_col)
    
    if flower_grid is not None:
        return flower_grid.tolist()
    else:
        return None