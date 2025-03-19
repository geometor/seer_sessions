"""
1.  **Identify Background:** Locate the bottom two rows of the input grid. These will remain unchanged.
2.  **Maintain Background:** Copy the identified two bottom rows directly to the output grid.
3.  **Construct rows to insert:**
    *   The first inserted row will be all 0.
    *   The second inserted row will be green (3) at opposite ends of the row, filling the remaining spaces with white (0).
    *   The third inserted row is the same at the second inserted row except the green elements (3) are adjacent to the end, filling the remaining spaces with white (0)
4.  **Combine:** insert the constructed rows at the top of the output.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    
    # Get dimensions of the input grid
    rows, cols = input_grid.shape
    
    # maintain background - bottom 2 rows are copied to output
    #background = input_grid[-2:, :]

    # construct first row to insert - all white (0)
    row1 = np.zeros(cols, dtype=int)

    # construct second row to insert - green at ends, rest white
    row2 = np.zeros(cols, dtype=int)
    row2[0] = 3
    row2[-1] = 3
    
    # construct third row to insert - green adjacent to ends, rest white
    row3 = np.zeros(cols, dtype=int)
    row3[1] = 3
    row3[-2] = 3

    # build output grid from constructed rows
    output_grid = np.vstack((row1, row2, row3, input_grid[-2:,:]))


    return output_grid