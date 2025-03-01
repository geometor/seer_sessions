# 234bbc79 • 006 • refine_coder

---
```python
"""
1.  **Identify and Remove Gray Pixels:** Locate all gray (5) pixels in the input grid.
2.  **Shift Pixels Left:** For each row, remove the gray pixels. Shift all pixels to the *right* of each removed gray pixel one position to the left for each removed pixel.
3.  **Reduce Grid Width:** The final grid's width is reduced by the number of gray pixels removed. The final output has no gray pixels.
4.  Preserve all other pixels as they are shifted.
"""

import numpy as np

def get_gray_positions(grid):
    # returns a list of (row, col) tuples of positions with gray color
    return np.argwhere(grid == 5)

def shift_left(grid, row):
    """Shift elements to the left after removing grey pixels."""
    new_row = np.copy(grid[row,:])
    new_row = new_row[new_row != 5]  #remove all gray
    padding = np.zeros(grid.shape[1] - new_row.shape[0], dtype=int) #calculate padding
    new_row = np.concatenate((new_row, padding)) #append padding
    return new_row

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # get positions of the gray pixels in the grid
    gray_positions = get_gray_positions(input_grid)
    num_grays = len(gray_positions)

    # remove gray pixels by and shifting to the left, by row
    for r in range(input_grid.shape[0]):
      output_grid[r] = shift_left(output_grid, r)

    # remove the extra end columns created by the shift, equal to count of removed
    output_grid = output_grid[:, :input_grid.shape[1]-num_grays]

    return output_grid
```
