"""
Replaces gray (5) pixels with green (3) pixels based on their position
relative to white pixels in a checkerboard-like pattern, excluding 
some edge cases.
"""

import numpy as np

def get_adjacent_pixels(grid, row, col):
    """
    Gets the values of adjacent pixels (up, down, left, right).
    Returns a dictionary with keys 'up', 'down', 'left', 'right' and 
    corresponding pixel values.
    Returns -1 for out-of-bounds neighbors.
    """
    rows, cols = grid.shape
    adjacent = {}
    
    adjacent['up'] = grid[row - 1, col] if row > 0 else -1
    adjacent['down'] = grid[row + 1, col] if row < rows - 1 else -1
    adjacent['left'] = grid[row, col - 1] if col > 0 else -1
    adjacent['right'] = grid[row, col + 1] if col < cols - 1 else -1

    return adjacent

def transform(input_grid):
    """
    Transforms the input grid according to the specified rule.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    for row in range(rows):
        for col in range(cols):
            if input_grid[row, col] == 5:  # Check if it's a gray pixel
                adjacent = get_adjacent_pixels(input_grid, row, col)
                
                # Check for two horizontal white neighbors.
                horizontal_white_count = 0
                if adjacent['left'] == 0:
                    horizontal_white_count += 1
                if adjacent['right'] == 0:
                    horizontal_white_count += 1

                # Check for two vertical white neighbors.
                vertical_white_count = 0;
                if adjacent['up'] == 0:
                    vertical_white_count += 1
                if adjacent['down'] == 0:
                    vertical_white_count += 1
                    
                
                # Apply the replacement rule, excluding edge columns
                if row == 0 and vertical_white_count == 2 and 0 < col < cols-1:
                     output_grid[row,col] = 3;
                elif row == rows -1 and horizontal_white_count == 2 and 0 < col < cols-1:
                     output_grid[row,col] = 3;
                elif row == 0 and horizontal_white_count == 2 and 0 < col < cols-1 :
                     output_grid[row, col] = 3
                

    return output_grid