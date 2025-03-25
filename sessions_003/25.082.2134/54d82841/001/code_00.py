"""
Copies the input grid to the output grid, then conditionally adds yellow (4) pixels in the last row. 
Yellow pixels are added to a column in the last row only if that column contains at least one non-zero pixel in the rows above.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through columns
    for j in range(cols):
        # Check for non-zero elements in the column above the last row
        non_zero_found = False
        for i in range(rows - 1):
            if input_grid[i, j] != 0:
                non_zero_found = True
                break
        
        # Modify the last row based on the presence of non-zero elements
        if non_zero_found:
            output_grid[rows - 1, j] = 4

    return output_grid.tolist()