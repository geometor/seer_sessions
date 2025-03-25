"""
Transforms green pixels in the top region of the input grid to red if they are adjacent to white pixels (in the current or preceding row), otherwise to white. The top region is defined as the area above the first solid horizontal line of blue pixels. If no such line exists, return an empty array.
"""

import numpy as np

def find_boundary_row(input_grid):
    """Finds the row index of the first solid horizontal line of blue pixels."""
    for i, row in enumerate(input_grid):
        if np.all(row == 1):
            return i
    return -1

def get_adjacent_pixels(grid, r, c):
    """Gets the values of adjacent pixels in the current and preceding row."""
    rows, cols = grid.shape
    adjacent = []
    
    # Previous row
    if r > 0:
        for dc in [-1, 0, 1]:
            if 0 <= c + dc < cols:
                adjacent.append(grid[r-1, c+dc])
                
    # Same row
    for dc in [-1, 1]:
        if 0 <= c + dc < cols:
            adjacent.append(grid[r, c + dc])

    return adjacent

def transform(input_grid):
    input_grid = np.array(input_grid)
    boundary_row = find_boundary_row(input_grid)

    # If no boundary is found, return empty array
    if boundary_row == -1:
        return np.zeros((0, input_grid.shape[1]), dtype=int).tolist()

    # Trim the grid to the top region
    top_region = input_grid[:boundary_row]
    output_grid = np.copy(top_region)

    rows, cols = top_region.shape

    # Transform green pixels in the top region
    for r in range(rows):
        for c in range(cols):
            if top_region[r, c] == 3:
                adjacent_pixels = get_adjacent_pixels(top_region, r, c)
                if 0 in adjacent_pixels:
                    output_grid[r, c] = 2  # Change to red
                else:
                    output_grid[r, c] = 0  # Change to white

    return output_grid.tolist()