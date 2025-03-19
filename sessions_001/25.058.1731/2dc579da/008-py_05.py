"""
Locates the single yellow pixel in the input grid and extracts the 2x2 subgrid centered on that pixel, forming the output grid.  Edge cases where the yellow pixel is near the boundary are handled by effectively "wrapping" or taking only the available pixels.
"""

import numpy as np

def get_2x2_subgrid(grid, center_row, center_col):
    """Extracts a 2x2 subgrid centered around the given coordinates."""
    rows, cols = len(grid), len(grid[0])
    subgrid = []

    # Calculate the row and column indices for the subgrid, handling edge cases.
   
    r1 = center_row
    r2 = center_row + 1
    c1 = center_col
    c2 = center_col + 1    

    row1 = []
    row1.append(grid[r1%rows][c1%cols])
    row1.append(grid[r1%rows][c2%cols])
    subgrid.append(row1)

    row2 = []
    row2.append(grid[r2%rows][c1%cols])
    row2.append(grid[r2%rows][c2%cols])
    subgrid.append(row2)

    return subgrid
    

def find_yellow_pixel(grid):
    """Finds the coordinates of the single yellow pixel."""
    for r, row in enumerate(grid):
        for c, pixel in enumerate(row):
            if pixel == 4:
                return (r, c)
    return None  # Should not happen, based on problem description

def transform(input_grid):
    # Find the yellow pixel.
    yellow_pos = find_yellow_pixel(input_grid)

    # Extract the 2x2 subgrid centered on the yellow pixel.
    output_grid = get_2x2_subgrid(input_grid, yellow_pos[0], yellow_pos[1])

    return output_grid