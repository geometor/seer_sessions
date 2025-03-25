"""
1.  **Reflect:** Reflect the input grid horizontally. This means to swap the positions of elements across the central vertical axis. The leftmost column becomes the rightmost, and so on.

2.  **Conditional Color Replacement:** After reflection, iterate through each cell of the *reflected* grid. Check the *original* input grid:
    *   If a cell in the *original* grid was a 7 or a 2, *and* the corresponding position in the reflected grid is in the *left half* of the reflected grid (column index < width / 2), then change the reflected grid cell's value to 0.
    *   note, in the event that the grid has an odd width, the middle cell will be included in the left half by virtue of integer division.

3.  Return the modified reflected grid.
"""

import numpy as np

def reflect_horizontally(grid):
    """Reflects a grid horizontally."""
    return np.fliplr(grid)

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = reflect_horizontally(input_grid)
    width = output_grid.shape[1]

    # change output pixels 
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            # find original coordinates
            original_j = width - 1 - j
            if (input_grid[i, original_j] == 7 or input_grid[i, original_j] == 2) and j < width / 2:
                output_grid[i,j] = 0
    

    return output_grid.tolist()