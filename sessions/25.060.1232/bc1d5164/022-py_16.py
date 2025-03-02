"""
The transformation extracts the smallest square region containing all the yellow pixels, 
and scales down by removing blank rows and columns, and filling background with white.
"""

import numpy as np

def get_yellow_pixels(grid):
    """Finds the coordinates of all yellow pixels (value 4) in the grid."""
    yellow_pixels = []
    for r, row in enumerate(grid):
        for c, value in enumerate(row):
            if value == 4:
                yellow_pixels.append((r, c))
    return yellow_pixels

def transform(input_grid):
    """Transforms the input grid by extracting the smallest square containing all yellow pixels."""
    
    # Find coordinates of all yellow pixels.
    yellow_pixels = get_yellow_pixels(input_grid)
    
    # Determine bounding box.
    if not yellow_pixels:
        return []
    
    rows, cols = zip(*yellow_pixels) # separate row and col coordinates
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)

    # determine max size of square to hold all yellow pixels    
    height = max_row - min_row + 1
    width  = max_col - min_col + 1
    output_size = max(height, width)

    # Create a new output grid, pre-filled with white (0)
    output_grid = np.zeros((output_size, output_size), dtype=int)

    # Copy the yellow pixels to the new grid.
    for r, c in yellow_pixels:
        output_grid[r - min_row, c - min_col] = 4
    
    return output_grid.tolist()