```python
"""
1.  **Find the Cursor:** Locate the first instance of the digit `5` (gray) in the input grid. This is the starting position of the "cursor".
2.  **Trace and Collect:**  Move the cursor diagonally down and to the right, one cell at a time.  As the cursor moves, record the *values* of the cells it traverses, *including* the initial `5`.
3. **Initialize:** The output is filled with 0.
4.  **Output Placement:** Starting at the top-left corner (0,0) of the *output* grid:
    *   Place a `5`.
    *   Iterate through the collected values *excluding* the first value (the initial 5). Place the collected value *to the left* of the current `5`.
    *   Move the cursor one cell diagonally down and to the right in the *output* grid.
    *   Repeat placing a '5', and placing the *next* collected value, from left to right.
5.  **Termination:** Stop when the cursor reaches the edge of the output grid (either the rightmost column or the bottom row).  Any remaining cells in the output grid remain `0`.
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
    replacement_index = 1 # skip first 5
    while cursor_row_out < rows and cursor_col_out < cols:
        output_grid[cursor_row_out, cursor_col_out] = 5
        # place prior elements
        place_col = cursor_col_out - 1
        for p_index in range(replacement_index):
            if place_col >= 0:
                output_grid[cursor_row_out,place_col] = replacement_values[p_index]
                place_col -=1

        cursor_row_out += 1
        cursor_col_out += 1

        if replacement_index < len(replacement_values):
            replacement_index+=1
        

    return output_grid
```