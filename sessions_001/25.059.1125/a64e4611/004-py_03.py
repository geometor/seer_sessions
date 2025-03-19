"""
1.  **Identify the Boundary:** Find the rectangular boundary formed by color '8' (azure).
2.  **Identify Internal Regions:** Within this boundary, identify all regions of color '0' (white).
3.  **Connect and Fill:** Change all '0' (white) pixels to '3' (green) *only if* they are part of a continuous region of 0s that is adjacent to a non-0, and non-8, color. This effectively fills the space between other colors and the '8' boundary with '3'.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """
    Get the valid neighbors (up, down, left, right) of a cell in a grid.
    """
    rows, cols = grid.shape
    neighbors = []
    if row > 0:
        neighbors.append((row - 1, col))
    if row < rows - 1:
        neighbors.append((row + 1, col))
    if col > 0:
        neighbors.append((row, col - 1))
    if col < cols - 1:
        neighbors.append((row, col + 1))
    return neighbors

def flood_fill_conditional(grid, row, col, target_color, replacement_color):
    """
    Performs a conditional flood fill operation.
    Replaces target_color with replacement_color starting from (row, col) only if
    the region is connected to a non-target, non-boundary color.
    """
    rows, cols = grid.shape
    if row < 0 or row >= rows or col < 0 or col >= cols or grid[row, col] != target_color:
        return False

    # Check for connection to a non-target, non-8 color
    connected = False
    for neighbor_row, neighbor_col in get_neighbors(grid, row, col):
        neighbor_color = grid[neighbor_row, neighbor_col]
        if neighbor_color != target_color and neighbor_color != 8:
            connected = True
            break
    
    if not connected:
        return False
    
    grid[row, col] = replacement_color
    
    flood_fill_conditional(grid, row - 1, col, target_color, replacement_color)
    flood_fill_conditional(grid, row + 1, col, target_color, replacement_color)
    flood_fill_conditional(grid, row, col - 1, target_color, replacement_color)
    flood_fill_conditional(grid, row, col + 1, target_color, replacement_color)
    
    return True

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Iterate through the grid, looking for 0s to fill
    for r in range(rows):
        for c in range(cols):
            if output_grid[r, c] == 0:
                # Attempt conditional flood fill, only changing if connected to a non-0, non-8 color.
                flood_fill_conditional(output_grid, r, c, 0, 3)
    
    return output_grid