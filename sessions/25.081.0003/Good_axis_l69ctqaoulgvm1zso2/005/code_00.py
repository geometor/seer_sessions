"""
Replaces white pixels in columns containing white with azure pixels based on the position of a horizontal line of red and azure pixels, and whether there are any azure pixels below that line in the same column.
"""

import numpy as np

def find_control_row(grid):
    # Find the row that has all reds and one azure
    rows, cols = grid.shape
    for r in range(rows):
        unique_colors = np.unique(grid[r, :])
        if len(unique_colors) == 2 and np.all(np.isin(unique_colors, [2, 8])):
             if np.sum(grid[r,:] == 8) == 1: # Check for a single azure
                return r
    return -1

def find_white_columns(grid):
    #find columns that have at least one white pixel
    rows, cols = grid.shape
    white_cols = []
    for c in range(cols):
        if np.any(grid[:,c] == 0):
            white_cols.append(c)

    return white_cols

def find_azure_below(grid, row, col):
    rows,cols = grid.shape
    for r in range(row, rows):
        if grid[r,col] == 8:
            return True
    return False
    

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    grid = np.array(input_grid)  # Convert to NumPy array for easier manipulation
    rows, cols = grid.shape
    output_grid = np.copy(grid)  # Initialize output_grid as a copy of input_grid

    control_row_index = find_control_row(grid)
    
    if control_row_index != -1:
        white_cols = find_white_columns(grid)
        # Apply the replacement rule
        for r in range(control_row_index):
            for c in white_cols:
                if output_grid[r, c] == 0:
                    if not find_azure_below(grid, control_row_index, c):
                        output_grid[r,c] = 8
                    else:
                        output_grid[r,c] = 0

    return output_grid.tolist()