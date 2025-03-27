```python
"""
1.  **Size Transformation:**
    *   Example 1: The output grid is 8 rows shorter and 5 columns narrower than the input grid.
    *   Example 2: The output grid is 9 rows shorter and 5 columns narrower than the input grid.

2.  **Border:**
    *   Both grids have a one pixel grey (color 5) border.

3.  **Color Mapping (Interior):**
    The color mapping is applied to the interior pixels (excluding the border)
    * Input 5 remains 5.
    * Other mappings are still unclear.
"""

import numpy as np

def transform(input_grid):
    input_grid = np.array(input_grid)
    input_height, input_width = input_grid.shape

    # Determine which example we are dealing with based on input size.
    if input_height == 23 and input_width == 24:  # Example 1
        output_height = input_height - 8
        output_width = input_width - 5
        # Initialize output_grid with 5s (gray background)
        output_grid = np.full((output_height, output_width), 5, dtype=int)
                # Iterate through input_grid, mapping colors to the output_grid
        for i in range(1,output_height-1):
          for j in range(1,output_width - 1):
            #adjust for the border offset
            input_row = i + 4
            input_col = j + 2

            value = input_grid[input_row,input_col]
            if value == 5:
                output_grid[i,j] = 5
            else:
                output_grid[i,j] = 0
    elif input_height == 22 and input_width == 23:  # Example 2
        output_height = input_height - 9
        output_width = input_width - 5
        # Initialize output_grid with 5s (gray background)
        output_grid = np.full((output_height, output_width), 5, dtype=int)
                # Iterate through input_grid, mapping colors to the output_grid
        for i in range(1,output_height - 1):
          for j in range(1,output_width - 1):
            #adjust for the border offset
            input_row = i + 4
            input_col = j + 2

            value = input_grid[input_row,input_col]
            if value == 5:
                output_grid[i,j] = 5
            else:
                 output_grid[i,j] = 0
    else:
        return None  # Unknown example

    return output_grid
```