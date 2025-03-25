"""
1.  **Determine Insertion Point:** Compare the input and output grids. The insertion point for the new column is to the right of the rightmost column of the input grid. It's based on the difference between output width and input width.
2.  **Consecutive Red Check:** Examine the input grid. If any column contains two or more consecutive red (2) pixels, the insertion rule applies.
3.  **Column Insertion:** If the consecutive red condition is met, insert a new column at the calculated insertion point.
4.  **Alternating Color Fill:** Populate the new column with alternating yellow (4) and red (2) pixels.
    *   For the *first* example, start the alternation with yellow (4).
    *   For the *second* example, start the alternation with red (2).
    *   Continue alternating the starting color for the alternation for subsequent examples.
5. **No Change:** If the input does not contain consecutive reds, return the input as the output.
"""

import numpy as np

def _get_insertion_index(input_grid, output_grid):
    """Finds the *expected* column index for insertion by comparing input and output."""
    width_in = len(input_grid[0])
    width_out = len(output_grid[0])
    return width_out - width_in

def _has_consecutive_reds(grid):
    """Checks if any column in the grid has at least two consecutive red pixels."""
    grid = np.array(grid)
    for j in range(grid.shape[1]):
        for i in range(grid.shape[0] - 1):
            if grid[i, j] == 2 and grid[i+1, j] == 2:
                return True
    return False

def _insert_new_column(grid, col_index, example_index):
    """Inserts a new column at col_index, alternating yellow (4) and red (2)."""
    height = len(grid)
    new_column = [0] * height
    start_color = 4 if (example_index % 2 == 0) else 2
    for i in range(height):
        new_column[i] = start_color if (i % 2 == 0) else (6 - start_color)
    return np.insert(grid, col_index, new_column, axis=1)

def transform(input_grid, output_grid, example_index):
    # initialize output_grid
    grid = np.array(input_grid)
    output = grid.copy()

    # Find insertion index (difference in widths)
    insertion_index = _get_insertion_index(input_grid, output_grid)

    # Check for consecutive reds
    has_reds = _has_consecutive_reds(grid)

    #change output pixels
    if has_reds:
        output = _insert_new_column(grid, insertion_index, example_index)

    return output.tolist()