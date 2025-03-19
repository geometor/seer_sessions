"""
1.  **Check for Change:** If the input grid contains the color blue (value 1), proceed to step 2. Otherwise, the output is identical to the input.
2.  **Extract Subgrid:** Extract the 4x4 subgrid located at the top-left corner of the input grid.
3.  **Conditional Color Change:**
     *   If the color blue (1) exists within the original *input* grid, replace all values of 1 in the extracted 4x4 *output* with 0. All other colors in the 4x4 subgrid are unchanged from the input.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid - if no change, input is output
    output_grid = np.copy(input_grid)

    # Check for Change: If blue (1) is present in the input grid.
    if np.any(input_grid == 1):
        # Extract Subgrid: 4x4 subgrid at the top-left corner.
        subgrid = input_grid[:4, :4]
        output_grid = np.copy(subgrid)

        # Conditional Color Change: Replace 1 with 0 in the subgrid.
        output_grid[output_grid == 1] = 0
    
    # if the input contains a 1, then we truncate to 4x4
    if np.any(input_grid==1):
        return output_grid
    else:
        return output_grid

