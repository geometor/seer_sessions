"""
1. **Identify the blue line:** Locate the vertical line of blue (1) pixels in the input grid. Note its column index (starting from 0). in this case, 3.
2.  **Extract and check first element**: Get the first row element from the input_grid, and see it's color.
3.  **Create Output Grid:** if the color of the checked element is not 0, take the row index, change the input_grid color 1 to 8, and fill that column with the new color. else, fill with 0.
4. The height of the output grid is same to the input grid.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    rows = len(input_grid)
    cols = 3
    output_grid = np.zeros((rows, cols), dtype=int)
    
    # Extract and check first element
    first_row_element = input_grid[0]

    for i in range(len(first_row_element)):
        # fill with the new color if not 0
        if first_row_element[i] != 0:
          if first_row_element[i] == 1:
            new_color = 8
          else:
            new_color = first_row_element[i]
          
          col_index = i % 3
          
          output_grid[:, col_index] = new_color

    return output_grid