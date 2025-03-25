```python
"""
1.  **Find the Red Base:** Identify the single horizontal red line (color 2) within the input grid. Record its row index (`red_row`), starting column (`red_start`), and ending column (`red_end`).

2.  **Create Green Triangle:**
    *   Iterate from the row immediately *above* the red line (`red_row` - 1) up to row 0.
    *   For each row `i`, fill with green (color 3) from column 0 up to column (`red_start + (red_row - 1 - i)`). This correctly extends the green triangle to the right.

3.  **Create Blue Triangle:**
    *   Iterate from the row immediately *below* the red line (`red_row` + 1) down to the last row of the grid.
    *   For each row `i`, calculate a starting column `blue_start = i - red_row`.
     Fill with blue (color 1) from column blue_start to column red_end - (i - (red_row +1))
"""

import numpy as np

def find_red_object(grid):
    # Find the row index and starting/ending column indices of the red object.
    for r_idx, row in enumerate(grid):
        if 2 in row:
            c_start = np.where(row == 2)[0][0]
            c_end = np.where(row == 2)[0][-1]
            return r_idx, c_start, c_end
    return None, None, None

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find the red object
    red_row, red_start, red_end = find_red_object(input_grid)

    if red_row is None:  # Handle cases where there's no red object
        return output_grid

    # Create green object
    for i in range(red_row - 1, -1, -1):
        green_end = red_start + (red_row - 1 - i)
        output_grid[i, 0:min(green_end + 1,cols)] = 3

    # Create the blue object
    for i in range(red_row + 1, rows):
        blue_start = i - red_row -1
        blue_end = red_end - (i - (red_row + 1))
        if blue_end >= 0 and blue_start < cols:
            output_grid[i, max(0,blue_start +1):min(blue_end + 1, cols)] = 1

    return output_grid
```