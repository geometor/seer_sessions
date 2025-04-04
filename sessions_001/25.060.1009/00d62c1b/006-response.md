# 00d62c1b • 006 • refine_coder

---
```python
"""
The transformation rule is to insert a yellow (4) pixel between any two adjacent green (3) pixels in the horizontal or vertical direction. If there are no green pixels, the output is identical to the input.
"""

import numpy as np

def insert_row(grid, row_index, color):
    """Inserts a new row of the specified color at the given row index."""
    rows, cols = grid.shape
    new_row = np.full((1, cols), color)
    return np.insert(grid, row_index, new_row, axis=0)

def insert_col(grid, col_index, color):
    """Inserts a new column of the specified color at the given column index."""
    rows, cols = grid.shape
    new_col = np.full((rows, 1), color)
    return np.insert(grid, col_index, new_col, axis=1)

def transform(input_grid):
    # Initialize output_grid. Start by copying the input.
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Keep track of insertions to avoid shifting indices.
    row_insertions = 0
    col_insertions = 0

    # Iterate through the original grid to find adjacent greens.
    for row in range(rows):
        for col in range(cols):
            if input_grid[row, col] == 3:
                # Check for vertical adjacency
                if row + 1 < rows and input_grid[row + 1, col] == 3:
                    output_grid = insert_row(output_grid, row + 1 + row_insertions, 4)
                    row_insertions += 1

    # reset insertions for column check
    rows, cols = input_grid.shape #original
    temp_grid = np.copy(input_grid)
    col_insertions = 0

    for row in range(rows):
        for col in range(cols):
            if input_grid[row,col] == 3:
                # Check for horizontal adjacency.
                if col + 1 < cols and input_grid[row, col + 1] == 3:
                    temp_grid = insert_col(temp_grid, col + 1 + col_insertions, 4)
                    col_insertions += 1
    
    # combine row and col insertions
    rows, cols = temp_grid.shape
    row_insertions = 0
    for row in range(rows):
        for col in range(cols):
            if temp_grid[row,col] == 3:
                if row + 1 < rows and temp_grid[row+1,col] == 3:
                    output_grid = insert_row(output_grid, row+1+row_insertions,4)
                    row_insertions +=1

    return output_grid
```
