"""
1.  **Identify Regions:** Divide the input grid into two regions: a "blue region" in the top-left and a "red region" in the bottom-right.
2. **Color Swap, Blue with white:** Scan the original "Blue Region". Inside that region, search for white pixels (0). If some are to the right of the blue pixels and above the main horizontal center, then change the blue pixel to it's right, to red (2)
3.  **Color Swap, Blue with Red:**. Scan the original "Red Region". Inside that region, search for white pixels (0). If some are to the left of red pixels (2), swap the color of those red pixel for blue.
4. Leave the rest as is
"""

import numpy as np

def transform(input_grid):
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through the "blue region" (top-left)
    for r in range(rows):
        for c in range(cols):
            #color swap in top region
            if input_grid[r,c] == 0 and c>0 and input_grid[r,c-1] == 1 and r <4:
                output_grid[r,c-1] = 2

            if input_grid[r, c] == 0 and  c < cols - 1 and input_grid[r, c + 1] == 2 and r>4:
                output_grid[r, c + 1] = 1
    return output_grid