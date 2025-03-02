"""
1.  **Preserve Existing Elements:** Copy the entire input grid to the output grid without modification.
2.  **Identify Target Location:** Find the lowest row and rightmost column within the grid where a two-pixel "L" shape (one pixel above and one to the left of another) can be placed *without* overwriting any existing non-background colored pixels.
3.  **Add Green "L":** Place a green "L" shape, consisting of two green pixels, at the identified location. The "L" should be oriented with one pixel directly above the other, and the bottom pixel should be in the identified row and column.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    
    # get dimensions
    height = output_grid.shape[0]
    width = output_grid.shape[1]

    # Find the lowest, rightmost available position for the "L"
    for r in range(height - 1, -1, -1):
        for c in range(width - 1, -1, -1):
            # Check if we can place the "L" here without overwriting
            if output_grid[r, c] == 0 and output_grid[r-1,c] == 0: # Check current and above
                output_grid[r, c] = 3
                output_grid[r-1, c] = 3
                return output_grid

    return output_grid