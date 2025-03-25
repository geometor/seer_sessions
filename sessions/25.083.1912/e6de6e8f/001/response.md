```python
"""
1.  **Initialization:** Create an output grid initialized entirely with white (0) pixels. The width of the output grid is fixed at 7 columns. The height is variable but we observe that it doubles the input column number and subtract 4, for the 3 examples we have $2n - 4$ where $n$ is the number of columns of the input.
2.  **Green Pixel Placement:** Place a single green (3) pixel in the first row, fourth column of the output grid.
3.  **Red Pixel Expansion:**
    *   Identify the x-coordinate of each red pixel within the top row of the *input* grid.
    *   For each x-coordinate found:
        *   In the *output* grid, at that same x-coordinate and fourth column:
            *   Place a red (2) pixel.
            *   Continue placing red pixels vertically downwards until the bottom of the grid.
    *   Identify the x-coordinate of each red pixel within the bottom row of the *input* grid.
            *   In the *output* grid, at that same x-coordinate and third column:
            *   Place a red (2) pixel.
            *   Continue placing red pixels vertically downwards until reaching the last row where the y coordinate (row number) is $height - number\ of\ red\ columns\ from\ bottom\ row$.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_height, input_width = input_grid.shape
    output_width = 7
    output_height = 2 * input_width - 4
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Place green pixel
    output_grid[0, 3] = 3

    # Find red pixel x-coordinates in the top row of the input
    top_red_x = [i for i, pixel in enumerate(input_grid[0]) if pixel == 2]

    # Expand red pixels downwards from the fourth row
    for x in top_red_x:
        output_grid[3:, x] = 2

    # Find red pixel x-coordinates in the bottom row of input
    bottom_red_x = [i for i, pixel in enumerate(input_grid[1]) if pixel == 2]
    
    num_bottom_red = len(bottom_red_x)

    for x_index, x in enumerate(bottom_red_x):
      for y in range(2, output_height - num_bottom_red + x_index + 1):
          output_grid[y,x] = 2
    

    return output_grid
```