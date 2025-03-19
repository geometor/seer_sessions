"""
1. Identify Key Colors: The key colors are all non-white colors present in the input grid.
2. Preserve Magenta: If magenta (6) is present in the input, it remains unchanged in the output.
3. Fill Remaining Cells: All white (0) cells in the output grid are filled with red (2) if red exists in the input grid, otherwise it is filled with magenta (6)
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Check if red (2) exists in the input grid
    if 2 in input_grid:
        fill_color = 2
    elif 6 in input_grid:
        fill_color = 6
    else:
        return output_grid #Should never happen based on training, but protects if it does.

    # Iterate through the grid
    for i in range(rows):
        for j in range(cols):
            # Preserve magenta
            if output_grid[i, j] == 6:
                continue  # Magenta remains unchanged
            # Fill remaining 0s
            elif output_grid[i, j] == 0:
                output_grid[i, j] = fill_color

    return output_grid