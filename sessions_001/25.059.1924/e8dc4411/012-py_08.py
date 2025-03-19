"""
Identify the contiguous region of green pixels in the input grid and expand it
downwards in an inverted triangle shape.
"""

import numpy as np

def get_green_region_coords(grid):
    """Returns the coordinates of all green pixels in the grid."""
    return np.argwhere(grid == 3).tolist()

def get_topmost_row(coords):
    """Returns the minimum row index from a list of coordinates."""
    if not coords:
        return None
    return min(coord[0] for coord in coords)

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Find the coordinates of all green pixels
    green_coords = get_green_region_coords(input_grid)

    # If no green pixels are found, return the original grid
    if not green_coords:
        return output_grid

    # Determine the topmost row of the green region
    topmost_row = get_topmost_row(green_coords)

    #find the columns in the topmost row
    topmost_cols = [coord[1] for coord in green_coords if coord[0] == topmost_row]
    
    if not topmost_cols:
        return output_grid
    
    #use the average as the center column
    center_col = int(np.mean(topmost_cols))

    # Expand the green region downwards
    for row in range(topmost_row + 1, output_grid.shape[0]):
        # Calculate the extent of the expansion
        expansion = row - topmost_row

        # Apply the expansion to the left and right
        for col in range(center_col - expansion, center_col + expansion + 1):
            if 0 <= col < output_grid.shape[1]:
                output_grid[row, col] = 3

    return output_grid