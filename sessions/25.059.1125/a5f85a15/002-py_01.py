"""
The transformation rule is: Locate diagonal lines of non-zero pixels in the input grid. 
Traverse each diagonal and change every other non-zero pixel to yellow (4).
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the specified rule.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    
    # Function to process a single diagonal
    def process_diagonal(row_start, col_start, row_dir, col_dir):
        row, col = row_start, col_start
        change = False
        while 0 <= row < rows and 0 <= col < cols:
            if input_grid[row, col] != 0:
                if change:
                    output_grid[row, col] = 4
                change = not change
            row += row_dir
            col += col_dir

    # Iterate through diagonals from top-left to bottom-right
    for i in range(rows):
        process_diagonal(i, 0, 1, 1)  # Start from first column
    for j in range(1, cols):
        process_diagonal(0, j, 1, 1)  # Start from first row

    # Iterate through diagonals from top-right to bottom-left
    for i in range(rows):
        process_diagonal(i, cols - 1, 1, -1) # Start from the last column
    for j in range(cols-1):
      process_diagonal(0, j, 1, -1)


    return output_grid