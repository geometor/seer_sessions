"""
1.  **Initialization:** Create an output grid with the same dimensions as the input grid, filled entirely with 0s.
2.  **Find Cursor:** Locate the first instance of the digit `5` (gray) in the input grid. This is the starting position of the "cursor".
3.  **Trace and Collect:** Starting from the cursor's position in the *input* grid, move the cursor diagonally down and to the right, one cell at a time. Record the values of the cells traversed, *including* the initial `5`. Stop tracing when the cursor reaches the edge of the *input* grid.
4.  **Output Placement:** Starting at the top-left corner (0, 0) of the *output* grid, replace the values along a diagonal path (down and to the right) with the sequence of values collected in step 3.
5. **Termination:** The output grid values should only be replaced if there are more replacement values, and stop if the diagonal replacement path goes beyond the grid boundaries.
"""

import numpy as np

def find_cursor(grid):
    # Find the first occurrence of 5 in the grid
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == 5:
                return (r, c)
    return None

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Find the starting position of the cursor (5)
    cursor_row, cursor_col = find_cursor(input_grid)
    if cursor_row is None:  # Handle cases with no 5.
      return output_grid

    # Trace path and collect replacement values
    replacement_values = []
    r, c = cursor_row, cursor_col
    
    while r < rows and c < cols:
        replacement_values.append(input_grid[r,c])
        r += 1
        c += 1
    
    # Move cursor and replace values in output grid
    cursor_row_out, cursor_col_out = 0, 0  #start output at 0,0

    for val in replacement_values:
        if cursor_row_out < rows and cursor_col_out < cols:
            output_grid[cursor_row_out, cursor_col_out] = val
            cursor_row_out += 1
            cursor_col_out += 1
        else:
            break
    

    return output_grid