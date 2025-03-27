"""
1.  **Reflect:** Reflect the input grid horizontally.
2.  **Conditional Color Replacement:** Iterate through each cell of the *reflected* grid.
    *   Check the cell at the *original* (pre-reflection) position in the input grid.
    *   If the *current* position in the reflected grid is on the left half (column index < width/2), and the original cell was on the right half (original column index >= width/2) then:
        * Examine the *original* (pre-reflection) grid. If the color in the original position is any of the colors present on the right half, replace the value with 0 in the reflected grid. Note: left half INCLUDES the middle pixel if there is one.
3.  Return the modified, reflected grid.
"""

import numpy as np

def reflect_horizontally(grid):
    """Reflects a grid horizontally."""
    return np.fliplr(grid)

def get_right_half_colors(grid):
    """Gets the unique colors present in the right half of the grid."""
    grid = np.array(grid)
    width = grid.shape[1]
    right_half = grid[:, width // 2:]
    return np.unique(right_half)

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = reflect_horizontally(input_grid)
    width = output_grid.shape[1]
    right_half_colors = get_right_half_colors(input_grid)

    # change output pixels 
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            # find original coordinates
            original_j = width - 1 - j
            if j < width / 2 and original_j >= width / 2:  # Corrected condition
                if input_grid[i, original_j] in right_half_colors:
                    output_grid[i,j] = 0
    

    return output_grid.tolist()