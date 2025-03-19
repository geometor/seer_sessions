"""
1.  **Identify the Core:** Locate the 2x2 block of non-zero pixels in the center of the input grid.
2.  **Preserve the Core**: Copy the 2x2 core block from the input to the identical location of the output grid
3.  **Mirror Top-Left:** Copy the value in the bottom right of the 2x2 core to the top-left 2x2 corner of the output grid.
4.  **Mirror Top-Right:** Copy the value in the bottom left of the 2x2 core to the top-right 2x2 corner of the output grid.
5.  **Mirror Bottom-Left:** Copy the value at the top right of the 2x2 core to the bottom-left 2x2 corner of the output grid.
6.  **Mirror Bottom-Right:** Copy the value in the top left of the 2x2 core to the bottom-right 2x2 corner of the output grid.
7. **Fill Remaining:** Keep all other cells in the output grid as 0 (white).
8. **Dynamic Corner Indexing:**
     - Top-left corner starts at row 0, column 0.
     - Top-right corner starts at row 0, column (width - 2).
     - Bottom-left corner starts at row (height - 2), column 0.
     - Bottom-right corner starts at row (height - 2), column (width - 2).
     - all corners extend 2x2
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid with zeros, same size as input.
    output_grid = np.zeros_like(input_grid)

    # Get the dimensions of the grid
    rows, cols = input_grid.shape

    # 1. & 2. Preserve the central 2x2 block
    #    Adjusted indexing to work for odd and even dimensions
    center_row = rows // 2
    center_col = cols // 2
    output_grid[center_row-1:center_row+1, center_col-1:center_col+1] = input_grid[center_row-1:center_row+1, center_col-1:center_col+1]

    # 3. Mirror Top-Left:  Bottom-right of core to top-left of output.
    output_grid[0:2, 0:2] = input_grid[center_row, center_col]
    
    # 4. Mirror Top-Right: Bottom-left of core to top-right of output
    output_grid[0:2, cols-2:cols] = input_grid[center_row, center_col-1]

    # 5. Mirror Bottom-Left: Top-right of core to bottom-left
    output_grid[rows-2:rows, 0:2] = input_grid[center_row-1, center_col]

    # 6. Mirror Bottom-Right: Top-left of core to bottom-right
    output_grid[rows-2:rows, cols-2:cols] = input_grid[center_row-1, center_col-1]


    return output_grid