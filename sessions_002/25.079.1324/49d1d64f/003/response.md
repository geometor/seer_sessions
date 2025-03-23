```python
"""
The output grid is created with a border of zeros and dimensions two greater than the input grid in both rows and columns. Each pixel in the input grid is copied to the output grid at a location offset by +1 row and +1 column. Some of these pixels are also expanded into 2x2 blocks.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid with zeros, 2 rows and 2 columns larger than input
    input_rows = len(input_grid)
    input_cols = len(input_grid[0])
    output_rows = input_rows + 2
    output_cols = input_cols + 2
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # Iterate through input grid
    for i in range(input_rows):
        for j in range(input_cols):
            # Get the pixel value from input
            pixel_value = input_grid[i][j]

            # Copy the pixel to its 'original' location in the output grid, +1 offset
            output_grid[i+1][j+1] = pixel_value
            
            # Duplicate the pixel to form a 2x2 block, *also* in the output grid, offset by 1
            # The logic to determine *which* pixels get expanded isn't clear yet,
            # so for now we expand all and expect failures
            output_grid[i+1][j+1] = pixel_value
            output_grid[i+1][j+2] = pixel_value
            output_grid[i+2][j+1] = pixel_value
            output_grid[i+2][j+2] = pixel_value

    return output_grid
```