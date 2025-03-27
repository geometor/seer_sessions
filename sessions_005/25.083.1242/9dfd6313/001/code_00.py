"""
1.  **Identify the "cursor":** Find the initial location of the digit `5` (gray) in the input grid. This may not be in the top-left corner.
2.  **Trace the cursor's path:** The cursor moves diagonally down and to the right. Determine the maximum diagonal path length for the `5`.
3. **Identify replacement values.** Record the values from the input, in order, from the cells where the `5` was located.
4.  **Construct the output grid:** Create an output grid of the same dimensions as the input grid, filled initially with 0.
5.  **Place the cursor and collected elements:** Move the cursor (5) diagonally on the output grid. Each time the `5` is placed, move to the next element in your list of input elements. Then, go back one space (left) on the row and place that next value. Continue this process until all the values in your list are exhausted.
6. **Cursor stops**: Once the cursor can't move further, you can stop.
7. **Remaining cells**: Leave any un-replaced output cell value as `0`.
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
    if cursor_row is None:  # Handle cases with no 5. Should probably never happen.
      return output_grid

    # Trace path and collect replacement values
    replacement_values = []
    r, c = cursor_row, cursor_col
    
    while r < rows and c < cols:
        replacement_values.append(input_grid[r,c])
        r += 1
        c += 1
    
    replacement_values.pop(0) # don't include the first `5`


    # Move cursor and replace values in output grid
    cursor_row_out, cursor_col_out = 0, 0  #start output at 0,0
    replacement_index = 0
    while cursor_row_out < rows and cursor_col_out < cols:
        output_grid[cursor_row_out, cursor_col_out] = 5
        # place prior elements
        place_col = cursor_col_out -1
        for p_index in range(replacement_index -1, -1, -1):
          if place_col >= 0:
            output_grid[cursor_row_out, place_col] = replacement_values[p_index]
            place_col -= 1

        cursor_row_out += 1
        cursor_col_out += 1
        if replacement_index < len(replacement_values):
              replacement_index+=1

    # copy the values from collected diagonal    
    r, c = cursor_row, cursor_col
    r_out, c_out = 0, 0
    replacement_values_index = 0
    while r < rows and c < cols:
      if replacement_values_index < len(replacement_values):
        output_grid[r_out, c_out] = 5
        inner_c = c_out -1
        for i in range(replacement_values_index):
            if inner_c >= 0:
              output_grid[r_out,inner_c] = replacement_values[i]
              inner_c -= 1
        replacement_values_index += 1
      r+=1
      c+=1
      r_out += 1
      c_out += 1


    return output_grid