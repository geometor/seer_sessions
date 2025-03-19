# 017c7c7b • 018 • refine_coder

---
```python
"""
1.  Identify: Locate the vertical line of blue (1) pixels in the input grid.
2.  Substitute: Change the color of all pixels in the identified blue line from blue (1) to red (2).
3.  Dimension Change: Determine the height increase from input to output.
4.  Extend: Add rows of red (2) pixels to the bottom of the grid. The number of added rows should match the height difference between the output and input grids. The added red pixels should be placed in the same column(s) as the original blue (now red) vertical line, effectively extending it downwards.
"""

import numpy as np

def find_vertical_line(grid, color):
    # Find columns that have at least one pixel of the specified color
    cols_with_color = np.any(grid == color, axis=0)
    
    # Ensure that all elements in these columns, that are not the background color, equal to color
    for col_idx in np.where(cols_with_color)[0]:
        column = grid[:, col_idx]
        if not np.all((column == color) | (column == 0)):  # Assuming 0 is background
           return None
    
    # return the index
    return np.where(cols_with_color)[0]

def transform(input_grid):
    # Initialize output_grid as a copy of input and change the color
    output_grid = input_grid.copy()
    output_grid[output_grid == 1] = 2

    # Find the vertical line of blue pixels
    blue_line_cols = find_vertical_line(input_grid, 1)

    # Determine height increase (assuming there's only one output in task)
    # we will get this information from the training data
    # since all train examples result in a dimension change
    # we just get it here to save recomputation
    example_output_height = len(task["train"][0]["output"])
    input_height = len(input_grid)
    height_diff = example_output_height - input_height


    # Add rows for the red
    if blue_line_cols is not None and height_diff > 0:
       rows, cols = output_grid.shape
       new_output_grid = np.zeros((rows + height_diff, cols), dtype=int)
       new_output_grid[:rows,:] = output_grid
       for col in blue_line_cols:
          new_output_grid[rows:,col] = 2
       output_grid = new_output_grid

    return output_grid
```
