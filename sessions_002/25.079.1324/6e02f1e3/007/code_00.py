"""
1.  **Examine the Input Grid:** Examine the entire input grid.
2. **Uniform Color Check**: If the input grid has the same color in all the cells, then put a row of 5's in the first row of output. Fill rest of the output grid with 0's.
3.  **Check for unique row values:** Check the number of unique colors per row.
    *  If there are three unique colors in each row, put 5's diagonally across the output
        * if the first row is the *smallest* color, put diagonal of 5's top left to bottom right
        * otherwise put diagonal of 5's top right to bottom left
    * Fill remaining cells with 0.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Uniform Color Check
    unique_colors = np.unique(input_grid)
    if len(unique_colors) == 1:
        output_grid[0, :] = 5
        return output_grid

    # Check for unique row values
    all_rows_unique = True
    for i in range(rows):
        if len(np.unique(input_grid[i, :])) != cols:
            all_rows_unique = False
            break

    if all_rows_unique:
        # Determine diagonal direction
        if input_grid[0,0] < input_grid[1,0]:  # Assuming at least two rows for comparison, based on examples
            for i in range(rows):
                output_grid[i, i] = 5
        else:
             for i in range(rows):
                output_grid[i, cols - 1 - i] = 5

    return output_grid