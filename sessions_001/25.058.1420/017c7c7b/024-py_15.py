"""
1. Replace all occurrences of blue (value 1) with red (value 2) in the input grid.
2. Create an exact copy of this modified grid.
3. Stack the copied, modified grid vertically below the original modified grid, resulting in a new grid that is twice the height of the original.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    # Create a copy of the input grid to modify. This will become the basis for the output.
    output_grid = np.copy(input_grid)

    # Replace all 1s (blue) with 2s (red)
    output_grid[output_grid == 1] = 2
    
    # Duplicate the entire modified grid
    duplicated_grid = np.copy(output_grid)

    # Vertically stack the duplicated grid below the modified grid
    output_grid = np.vstack((output_grid, duplicated_grid))

    return output_grid