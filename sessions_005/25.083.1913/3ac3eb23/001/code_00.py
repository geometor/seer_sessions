"""
The transformation takes each colored pixel and duplicates it at specific positions in output grid.

1.  **Identify**: Find all non-zero pixels (colored pixels) in the input grid.
2.  **Iterate:** For the height of the grid, repeat for each row:
3.  **Duplicate**: For each non-zero color, duplicate it: Copy the colored pixel's value.
4.  **Position**: Place one at the original x-coordinate (which represents the row) times 2. Place the other at one more than the original x-coordinate times 2.
5. **Fill Background:** Leave cells that are not filled empty

"""

import numpy as np

def transform(input_grid):
    # Initialize output grid with zeros, same size as input
    output_grid = np.zeros_like(input_grid)
    height = input_grid.shape[0]
    width = input_grid.shape[1]

    # Iterate through each cell of the input grid
    for y in range(height):
        n = 0
        for x in range(width):
            # Find non-zero pixels
            if input_grid[y, x] != 0:
                color = input_grid[y, x]

                # duplicate and position
                new_x_1 = 2 * n
                new_x_2 = 2*n + 1

                if new_x_1 < width:
                     output_grid[y,new_x_1] = color
                if new_x_2 < width:
                    output_grid[y,new_x_2] = color
                n += 1


    return output_grid