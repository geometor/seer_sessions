"""
The transformation involves finding the top-left 2x2 subgrid of non-white
pixels in the input, flipping this subgrid both horizontally and vertically
(equivalent to a 180-degree rotation), and using this flipped subgrid as the
output. If no such subgrid exists (all white), return a 1x1 white grid.
"""

import numpy as np

def get_top_left_non_white_subgrid(grid):
    """
    Finds the top-left 2x2 subgrid of non-white cells, moving to the right and then down.
    """
    rows, cols = grid.shape
    subgrid = []

    # Find the first non-white pixel's coordinates
    start_row = -1
    start_col = -1
    for r in range(0, rows):
        for c in range(0, cols):
            if grid[r, c] != 0:
                start_row = r
                start_col = c
                break
        if start_row != -1:
            break
    if start_row == -1: return np.array([[0]]) # Return default value of single white cell

    # Extract the 2x2 subgrid. Handle edge cases where the subgrid goes out of bounds
    if start_row + 1 < rows and start_col + 1 < cols:
        subgrid.append([grid[start_row, start_col],   grid[start_row, start_col+1]])
        subgrid.append([grid[start_row+1, start_col], grid[start_row+1, start_col+1]])
    elif start_row + 1 < rows: #can only add a 1x2
         subgrid.append([grid[start_row, start_col],   0])
         subgrid.append([grid[start_row+1, start_col], 0])
    elif start_col + 1 < cols: #can only add a 2x1
        subgrid.append([grid[start_row, start_col],   grid[start_row, start_col+1]])
        subgrid.append([0, 0])
    else: #a 1x1
        subgrid.append([grid[start_row, start_col],   0])
        subgrid.append([0, 0])

    return np.array(subgrid)
    

def transform(input_grid):
    """
    Transforms the input grid according to the described rule.
    """
    # Convert input grid to a NumPy array.
    input_np = np.array(input_grid)

    # Extract the top-left 2x2 non-white subgrid.
    extracted_grid = get_top_left_non_white_subgrid(input_np)

    # Flip the extracted grid horizontally and vertically (180-degree rotation).
    output_grid = np.flip(extracted_grid)

    return output_grid.tolist()