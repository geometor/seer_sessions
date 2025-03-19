"""
1.  **Identify the Core:** Locate the 2x2 block of non-zero pixels in the center of the input grid (rows 3-4, columns 3-4).
2.  **Preserve the Core**: Copy the 2x2 core block from the input to the identical location of the output grid
3.  **Mirror Top-Left:** Identify the colors represented by the value in the bottom right of the 2x2 core. Mirror these values to the top-left 2x2 corner of the output grid.
4.  **Mirror Top-Right:** Identify the colors represented by the value in the bottom left of the 2x2 core. Mirror these values to the top-right 2x2 corner of the output grid.
5.  **Mirror Bottom-Left:** Identify the colors represented by the values at the top right of the 2x2 core. Mirror these values to the bottom-left 2x2 corner of the output grid.
6.  **Mirror Bottom-Right:** Identify the colors represented by the values in the top left of the 2x2 core. Mirror these values to the bottom-right 2x2 corner of the output grid.
7. **Fill Remaining:** Keep all other cells in the output grid as 0 (white).
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid with zeros, same size as input.
    output_grid = np.zeros_like(input_grid)

    # Get the dimensions of the grid
    rows, cols = input_grid.shape

    # 1. & 2. Preserve the central 2x2 block
    output_grid[2:4, 2:4] = input_grid[2:4, 2:4]

    # 3. Mirror Top-Left:  Bottom-right of core to top-left of output.
    output_grid[0:2, 0:2] = input_grid[3, 3]  # input_grid[3][3]
    
    # 4. Mirror Top-Right: Bottom-left of core to top-right of output
    output_grid[0:2, 4:6] = input_grid[3, 2]

    # 5. Mirror Bottom-Left: Top-right of core to bottom-left
    output_grid[4:6, 0:2] = input_grid[2, 3]

    # 6. Mirror Bottom-Right: Top-left of core to bottom-right
    output_grid[4:6, 4:6] = input_grid[2, 2]


    return output_grid