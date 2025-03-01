"""
1.  **Input Grid Height**: Determine the height (number of rows) of the input grid.
2.  **Create Output Grid:** Create a new grid with a width of 3 columns and the height from the input grid.
3.  **Locate Green Square:** Identify the 2x2 green square in the input grid.  (Its position *does not* determine the output grid's size.)
4.  **Place Green Square:** Copy the 2x2 green square to the top-left corner (0, 0) of the output grid.
5.  **Add Green Column:** Fill the entire rightmost column (index 2) of the output grid with green pixels (value 3).
"""

import numpy as np

def transform(input_grid):
    # Determine the height of the input grid.
    input_height = len(input_grid)

    # Create an output grid with 3 columns and height equal to input height.
    output_grid = np.zeros((input_height, 3), dtype=int)

    # Place the 2x2 green square at the top-left of the output grid.
    output_grid[0:2, 0:2] = 3

    # Fill the rightmost column of the output grid with green.
    output_grid[:, 2] = 3

    return output_grid