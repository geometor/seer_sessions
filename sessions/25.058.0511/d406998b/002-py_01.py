"""
Examine the input grid. Identify all pixels with the value '5' (gray).
Change some of the pixels with value 5 to to the value '3' (green) using this logic:
Going from left-to-right, top-to-bottom, keep the first two gray pixels, then change the next one to green. Repeat this pattern.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    
    # Find the positions of all '5' (gray) pixels
    gray_positions = np.argwhere(input_grid == 5)
    
    # Counter for the pattern (keep 2, change 1)
    count = 0
    
    # Iterate through the positions and apply the transformation
    for pos in gray_positions:
        if count < 2:
            count += 1
        else:
            output_grid[pos[0], pos[1]] = 3
            count = 0

    return output_grid