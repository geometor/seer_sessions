"""
1.  **Border Creation**: The output grid has a one-pixel wide border of gray (5) color around its entire perimeter.
2.  **Interior Transformation:** The interior pixels of the output grid (excluding the border) are derived from the input grid with a specific color mapping.
3.  **Size Calculation:** The output height and width will be input height - 5 x input width - 5.
4.  **Color Mapping:**
    *   Input color 3 becomes output color 4.
    *   Input color 6 becomes output color 7.
    *   Input color 8 becomes output color 2.
    *   Input color 2 becomes output color 8.
    *   Input color 1 becomes output color 8.
    *  Input Color 4 becomes output color 2.
5.  **Default:** If a color in the input is not handled by the mapping above, then ignore it and move on.
"""

import numpy as np

def transform(input_grid):
    input_grid = np.array(input_grid)
    input_height, input_width = input_grid.shape

    # Calculate output dimensions.
    output_height = input_height - 5
    output_width = input_width - 5

    # Initialize output_grid with 5s (gray background)
    output_grid = np.full((output_height, output_width), 5, dtype=int)

    # Iterate through input_grid, mapping colors to the output_grid
    for i in range(output_height):
      for j in range(output_width):
        #adjust for the border offset
        input_row = i + 2
        input_col = j + 2
        
        value = input_grid[input_row,input_col]
        # Apply color transformations
        if value == 3:
            value = 4
        elif value == 6:
            value = 7
        elif value == 8:
            value = 2
        elif value == 2:
            value = 8
        elif value == 1:
            value = 8
        elif value == 4:
            value = 2

        output_grid[i, j] = value

    return output_grid