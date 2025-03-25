"""
The transformation expands connected lines of two or more red pixels to the edges of the input array. isolated red pixels, and other formations are left unchanged.
"""

import numpy as np

def get_red_regions(grid):
    """Finds all connected regions of '2' (red) pixels in the grid."""
    red_pixels = []
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == 2:
                red_pixels.append((r, c))
    return red_pixels

def is_connected_line(red_pixels, grid):
    """Checks if any of the red pixels are connected to the edge and form a line."""

    if not red_pixels:
        return False
    
    rows = [r for r, _ in red_pixels]
    cols = [c for _, c in red_pixels]
    
    if len(set(rows)) == 1 and len(red_pixels) > 1 :
        return True # horizontal line
    
    if len(set(cols)) == 1 and len(red_pixels) > 1:
            return True  # Vertical line

    return False  # Not a straight, connected line


def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    grid = np.array(input_grid)
    red_pixels = get_red_regions(grid)

    if is_connected_line(red_pixels, grid):

        rows = [r for r, _ in red_pixels]
        cols = [c for _, c in red_pixels]
        
        if len(set(rows)) == 1: #horizontal
            output_grid[rows[0], :] = 2  # Fill the entire row
        elif len(set(cols)) == 1:  #vertical
            output_grid[:, cols[0]] = 2    # Fill the entire column

    return output_grid.tolist()