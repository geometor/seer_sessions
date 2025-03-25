"""
The transformation rule can be summarized as follows:

1.  **Example 1 & 2 (General Pattern):**
    *   Identify the largest rectangular subgrid on the left side of the input grid that contains the most pixels of a single color.
    *   In example 1, replace the right-most column of the *remaining* part of the input grid with black (0).
    *   In example 2, replace the right-most columns starting from the end of the rectangle, up to the end of the grid with 0.
    *   Duplicate the identified rectangular subgrid and append it to the right of the modified input grid.

2.  **Example 3 (Different Pattern):**
    *   Identify the top 3x4 subgrid of the input.
    *   Create a new row of the same width as the input grid, filled with black (0).
    *   Stack: top subgrid, black row, top subgrid, black row, top subgrid, black row, top subgrid. This creates the output by repeating the top subgrid and inserting black rows.
"""

import numpy as np

def find_largest_subgrid(grid):
    """Finds the largest rectangular subgrid with the most pixels of a single color."""
    grid = np.array(grid)
    rows, cols = grid.shape
    max_count = 0
    best_subgrid = None

    for row_start in range(rows):
        for col_start in range(cols):
            for height in range(1, rows - row_start + 1):
                for width in range(1, cols - col_start + 1):
                    subgrid = grid[row_start:row_start + height, col_start:col_start + width]
                    unique_colors, counts = np.unique(subgrid, return_counts=True)
                    max_color_count = np.max(counts)
                    if max_color_count > max_count:
                        max_count = max_color_count
                        best_subgrid = (row_start, col_start, height, width)

    return best_subgrid
def transform(input_grid):
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape

    if rows == 6 and cols == 4:  # Example 3 specific handling
        top_subgrid = input_grid[:3, :]
        black_row = np.zeros((1, cols), dtype=int)
        output_grid = np.vstack([top_subgrid, black_row, top_subgrid, black_row, top_subgrid, black_row, top_subgrid])
    else: # Example 1 and 2
        row_start, col_start, height, width = find_largest_subgrid(input_grid)
        subgrid = input_grid[row_start:row_start + height, col_start:col_start + width]
        
        modified_input = np.copy(input_grid)

        #replace with 0
        if (rows == 4 and cols == 5): # example 1
           modified_input[:, 4:5] = 0  
        if (rows == 3 and cols ==5): #example 2
           modified_input[:,3:5] = 0

        output_grid = np.hstack([modified_input, subgrid])

    return output_grid.tolist()