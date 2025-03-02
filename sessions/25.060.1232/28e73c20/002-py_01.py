"""
Transforms an all-white input grid into a grid with a green (3) spiral pattern, leaving the inner parts white (0).
"""

import numpy as np

def transform(input_grid):
    """
    Transforms an all-white input grid into a grid with a green spiral pattern.
    """
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    def create_border(grid, start_row, end_row, start_col, end_col):
        # Create the outermost border
        grid[start_row:end_row + 1, start_col] = 3  # Left
        grid[start_row:end_row + 1, end_col] = 3  # Right
        grid[start_row, start_col:end_col + 1] = 3  # Top
        grid[end_row, start_col:end_col + 1] = 3  # Bottom
        return grid
    
    def insert_right(grid, start_row, end_row, start_col, end_col):
        #inserts green on rightmost column of remainder
        grid[start_row:end_row+1, end_col] = 3
        return grid

    start_row, start_col = 0, 0
    end_row, end_col = rows - 1, cols - 1

    while start_row <= end_row and start_col <= end_col:
        # create outer boundary
        output_grid = create_border(output_grid, start_row, end_row, start_col, end_col)
        
        start_row += 1
        start_col += 1
        end_row -= 1
        end_col -= 1

        # checks if next subgrid has all zeros before inserting partial boundary
        if start_row <= end_row and start_col <= end_col:
            if np.all(output_grid[start_row:end_row+1, start_col:end_col+1] == 0):
                output_grid = insert_right(output_grid, start_row, end_row, start_col, end_col)
            else:
                break

    return output_grid