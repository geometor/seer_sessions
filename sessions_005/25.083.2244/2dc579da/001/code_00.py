"""
Extract the region of the input grid *above* the single-color horizontal line that spans the entire width of the grid.
"""

import numpy as np

def find_dividing_line(grid):
    # Iterate through rows to find a full-width single-color horizontal line
    rows, cols = grid.shape
    for r in range(rows):
        if np.all(grid[r, :] == grid[r, 0]):  # Check if all elements in row are the same
            return r
    return -1  # No dividing line found

def transform(input_grid):
    """
    Transforms the input grid by extracting the region above the horizontal dividing line.
    """
    # Convert input grid to a NumPy array for easier manipulation
    grid = np.array(input_grid)
    
    # Find the row index of the dividing line
    dividing_line_row = find_dividing_line(grid)

    # If no dividing line is found, return an empty grid or handle appropriately. Here, returning original
    if dividing_line_row == -1:
        return input_grid

    # Extract the region above the dividing line
    output_grid = grid[:dividing_line_row, :]

    return output_grid.tolist()