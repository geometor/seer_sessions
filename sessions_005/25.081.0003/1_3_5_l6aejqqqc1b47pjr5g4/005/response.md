```python
"""
1.  **Identify Yellow Pixels:** Locate all pixels in the input grid with the color yellow (value 4).
2.  **Column-wise Propagation:** For each column in the grid:
    *   Iterate downwards, starting from the top row.
    *   If find yellow pixels and the next rows don't contain only yellow pixels, propagate downwards, setting to yellow each cell until the bottom of the grid is reached, or until to one row below the last row containing one or more yellow pixels.
    * If a row contains only yellow pixels, there is no propagation.
"""

import numpy as np

def find_yellow_pixels(grid):
    """Finds the coordinates of all yellow pixels in the grid."""
    return np.argwhere(grid == 4)

def transform(input_grid):
    """Transforms the input grid according to the waterfall rule."""
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate over each column
    for col in range(cols):
        last_yellow_row = -1
        # Find the last row index with a yellow pixel in *any* column.
        for row in range(rows):
            if 4 in input_grid[row, :]:
                last_yellow_row = row

        # Propagate yellow down in the current column
        for row in range(rows):
            if np.all(input_grid[row,:]==4): # check if all the current row is made by yellow cells
                break # do not propagate in this case
            if row <= last_yellow_row + 1:
               if input_grid[row, col] == 4: # propagate from yellow cells of input
                    output_grid[row, col] = 4
                    if row + 1 < rows:
                      output_grid[row + 1, col] = 4

    return output_grid.tolist()
```