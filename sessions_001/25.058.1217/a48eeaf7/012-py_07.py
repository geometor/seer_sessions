"""
Transforms the input grid by moving gray (5) pixels one step closer to the center of the grid, either horizontally or vertically, but only if a 2x2 red (2) square is present. If no red square is present, the output is identical to the input.
"""

import numpy as np

def find_red_square(grid):
    # Find the top-left corner coordinates of the red square
    rows, cols = grid.shape
    for r in range(rows - 1):
        for c in range(cols - 1):
            if grid[r, c] == 2 and grid[r+1, c] == 2 and grid[r, c+1] == 2 and grid[r+1, c+1] == 2:
                return (r, c)  # Return top-left corner
    return None

def find_gray_pixels(grid):
    # Find coordinates of all gray pixels
    return np.argwhere(grid == 5)

def calculate_center(grid):
    # Calculate the center coordinates of the grid
    rows, cols = grid.shape
    center_r = rows // 2
    center_c = cols // 2
    return (center_r, center_c)

def move_pixel(grid, row, col, center_row, center_col):
    # Move the pixel at (row, col) one step closer to the center
    new_grid = grid.copy()
    
    # only move if pixel is gray (5)
    if new_grid[row, col] != 5:
        return new_grid
    
    row_diff = abs(row - center_row)
    col_diff = abs(col - center_col)
    
    if row_diff > col_diff:
        # Move vertically
        if row < center_row:
            new_grid[row, col] = 0
            new_grid[row + 1, col] = 5
        else:
            new_grid[row, col] = 0
            new_grid[row - 1, col] = 5
    elif col_diff > 0: # handles edge case where diffs are equal
        # Move horizontally
        if col < center_col:
            new_grid[row, col] = 0
            new_grid[row, col + 1] = 5
        else:
            new_grid[row, col] = 0
            new_grid[row, col - 1] = 5
            
    return new_grid

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = input_grid.copy()

    # Find the red square
    red_square_corner = find_red_square(input_grid)

    # If no red square, return the input grid
    if red_square_corner is None:
        return output_grid

    # Find all gray pixels
    gray_pixels = find_gray_pixels(input_grid)

    # Calculate the center of the grid
    center_r, center_c = calculate_center(input_grid)

    # Iterate through gray pixels and move them towards the center
    for gray_r, gray_c in gray_pixels:
        output_grid = move_pixel(output_grid, gray_r, gray_c, center_r, center_c)
        
    return output_grid