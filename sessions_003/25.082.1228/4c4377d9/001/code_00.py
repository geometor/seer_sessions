"""
The input grid is reflected both horizontally and vertically, and then these reflections,
along with the original grid, are combined to form a new grid that is twice the size
of the original in both dimensions.
"""

import numpy as np

def reflect_vertical(grid):
    """Reflects the grid vertically."""
    return np.flipud(grid)

def reflect_horizontal(grid):
    """Reflects the grid horizontally."""
    return np.fliplr(grid)

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # Create a vertically mirrored copy of the input grid
    vertical_reflection = reflect_vertical(input_grid)

    # Create a horizontally mirrored copy of the input grid
    horizontal_reflection = reflect_horizontal(input_grid)

    # Create a combined horizontal and vertical reflection
    combined_reflection = reflect_horizontal(vertical_reflection)

    # Combine Rows:
    # 1. Combine original input's rows with its horizontal reflection
    top_rows = np.concatenate((input_grid, horizontal_reflection), axis=1)
    # 2. Combine the vertically reflected input's rows with the combined reflection
    bottom_rows = np.concatenate((vertical_reflection, combined_reflection), axis=1)

    # Combine grids: Combine the new rows vertically.
    output_grid = np.concatenate((top_rows, bottom_rows), axis=0)

    return output_grid.tolist()