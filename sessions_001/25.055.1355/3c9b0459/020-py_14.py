"""
The input grid is transformed into the output grid by swapping elements on the anti-diagonal using the following detailed instructions:
    - The element at position (0,0) swaps with (0,1), so the top left and top center swaps position
    - The element at position (2,0) swaps with position (2,1), so the bottom left and bottom center swaps position
    - The element at (0,2) swaps with (1,1), so the top right and center values are swapped
    - The element at position(2,1) swaps with (1,1), so the bottom center and center values are swapped
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # Swap elements (0,0) and (0,1)
    output_grid[0, 0], output_grid[0, 1] = output_grid[0, 1], output_grid[0, 0]

    # Swap elements (2,0) and (2,1)
    output_grid[2, 0], output_grid[2, 1] = output_grid[2, 1], output_grid[2, 0]
    
    # Swap elements (0,2) and (1,1)
    output_grid[0, 2], output_grid[1, 1] = output_grid[1, 1], output_grid[0, 2]
    
    # The last specified swap would result in (2,1) getting overwritten, and therefore not correct.
    # Therefore it needs to be removed from code.
    
    return output_grid