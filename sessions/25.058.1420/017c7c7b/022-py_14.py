"""
1. Replace all occurrences of the color blue (value 1) in the input grid with the color red (value 2).
2. Duplicate all of the rows of the modified grid.
3. Append the duplicated rows to the bottom of the modified grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    # Create a copy of the input grid to modify.  This will become the output grid.
    output_grid = np.copy(input_grid)

    # Replace all 1s (blue) with 2s (red)
    output_grid[output_grid == 1] = 2
    
    # Duplicate all rows
    duplicated_rows = np.copy(output_grid)

    # Add the duplicated rows to the bottom
    output_grid = np.vstack((output_grid, duplicated_rows))

    return output_grid