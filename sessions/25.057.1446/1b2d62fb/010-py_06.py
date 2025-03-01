"""
1. **Get First Row:** Extract the first row of the input grid. This row determines the colors and order of columns in the output grid.
2. **Create Output Grid:** Initialize an output grid with a height equal to the input grid's height and a width of 3.
3. **Iterate and Fill Columns:** Iterate through the first row elements.
    - If an element is not 0, it represents a color to be filled in a column of the output grid.
    - Determine the column index based on where we are in our iteration within the first 3 relevant colors (non-zero values).
    - Fill the entire corresponding column in the output grid with that color. if the element is 1, change it to 8.
4. **Return Output:** The output grid will have the same number of rows as the input and three columns, filled according to the non-zero colors from the first row of the input.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    rows = len(input_grid)
    cols = 3
    output_grid = np.zeros((rows, cols), dtype=int)
    
    # Extract and check first element
    first_row_element = input_grid[0]
    
    col_index = 0

    for i in range(len(first_row_element)):
        # fill with the new color if not 0
        if first_row_element[i] != 0:
          if first_row_element[i] == 1:
            new_color = 8
          else:
            new_color = first_row_element[i]
                    
          output_grid[:, col_index] = new_color
          col_index += 1
          if col_index >= 3:
            break

    return output_grid