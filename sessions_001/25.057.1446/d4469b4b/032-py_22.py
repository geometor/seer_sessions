"""
1.  **Identify Input:** Begin with a 5x5 input grid.
2.  **Locate Center:** Extract the 3x3 subgrid centered within the 5x5 input grid.
3.  **Transform Colors:**
    *   If a cell in the 3x3 subgrid of the input is red (2), change it to gray (5) in the output.
    *   If a cell in the 3x3 subgrid of the input is white (0), it remains white (0) in the output.
4. **Output:** Create the 3 x 3 output grid from the transformed colors
"""

import numpy as np

def get_center_subgrid(grid, subgrid_size):
    """
    Extracts a subgrid centered within the input grid.
    """
    grid_height, grid_width = grid.shape
    subgrid_height, subgrid_width = subgrid_size
    
    start_row = (grid_height - subgrid_height) // 2
    end_row = start_row + subgrid_height
    start_col = (grid_width - subgrid_width) // 2
    end_col = start_col + subgrid_width

    return grid[start_row:end_row, start_col:end_col]

def transform(input_grid):
    # initialize output_grid
    subgrid = get_center_subgrid(np.array(input_grid), (3,3))
    output_grid = np.zeros((3, 3), dtype=int)

    # change output pixels
    for i in range(3):
        for j in range(3):
            if subgrid[i,j] == 2:
                output_grid[i,j] = 5
            else:
                output_grid[i,j] = subgrid[i,j] # keep the original value (0 in this case)

    return output_grid