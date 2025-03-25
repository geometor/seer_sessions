"""
The transformation finds the right-most edge of non-zero horizontal regions and extends that edge downwards, 
replacing any existing '0' or the color directly below that edge.
"""

import numpy as np

def get_rightmost_pixel(input_grid, row, col):
    """
    Finds the rightmost pixel of a horizontal line of the same color starting at (row, col).
    """
    current_color = input_grid[row, col]
    if current_color == 0:
        return row, col
    
    while col + 1 < input_grid.shape[1] and input_grid[row, col + 1] == current_color:
        col += 1
    return row, col

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each cell in the input grid
    for row in range(rows):
        for col in range(cols):
            # if cell is non-zero, find the right-most edge of it
            if input_grid[row,col] != 0:
                rightmost_row, rightmost_col = get_rightmost_pixel(input_grid, row, col)

                # Propogate downwards
                for next_row in range(row + 1, rows):
                    output_grid[next_row, rightmost_col] = output_grid[rightmost_row,rightmost_col]
    return output_grid