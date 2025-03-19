"""
The program identifies an inner rectangle of non-black and non-azure pixels within an outer frame of azure pixels in the input grid.
It then reproduces this inner rectangle in the output grid, replacing the azure frame with black pixels.
"""

import numpy as np

def extract_inner_rectangle(grid):
    """
    Extracts the inner rectangle of non-black, non-azure pixels.
    """
    rows, cols = grid.shape
    
    # Find the boundaries of the inner rectangle
    top, bottom, left, right = -1, -1, -1, -1
    
    # Find top boundary
    for i in range(rows):
        if any(grid[i, j] != 8 and grid[i, j] != 0 for j in range(cols)):
            top = i
            break

    # Find bottom boundary
    for i in range(rows - 1, -1, -1):
        if any(grid[i, j] != 8 and grid[i, j] != 0 for j in range(cols)):
            bottom = i
            break
    
    # Find left boundary
    for j in range(cols):
        if any(grid[i, j] != 8 and grid[i, j] != 0 for i in range(rows)):
            left = j
            break
            
    # Find right boundary
    for j in range(cols-1, -1, -1):
        if any(grid[i, j] != 8 and grid[i, j] != 0  for i in range(rows)):
            right = j
            break
            
    if top == -1 or bottom == -1 or left == -1 or right == -1:
      return np.zeros_like(grid)

    # Extract the inner rectangle
    inner_rectangle = grid[top:bottom+1, left:right+1]
    return inner_rectangle

def transform(input_grid):
    """
    Extracts and reproduces the inner rectangle, replacing the azure frame with black.
    """
    # Extract the inner rectangle
    inner_rectangle = extract_inner_rectangle(input_grid)

    # Create an output grid of the same size as the input, filled with black
    output_grid = np.zeros_like(input_grid)
    
    rows_in, cols_in = input_grid.shape
    rows_ir, cols_ir = inner_rectangle.shape
    
    row_start = (rows_in-rows_ir)//2
    col_start = (cols_in - cols_ir)//2

    # Place the inner rectangle in the center of the output grid
    output_grid[row_start:row_start+rows_ir, col_start:col_start+cols_ir] = inner_rectangle

    return output_grid