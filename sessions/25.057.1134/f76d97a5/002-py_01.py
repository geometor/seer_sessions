"""
1. Iterate through each cell of the input grid.
2. If the cell value is 5 (gray), replace it with 0 (white).
3. If the cell value is 4 (yellow), retain the value (keep as 4).
4. The output grid has the same position for all colors.
5. Output will the modified grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule:
    - Replaces all occurrences of 5 (gray) with 0 (white).
    - Retains all occurrences of 4 (yellow).
    """
    output_grid = np.copy(input_grid)  # Create a copy to avoid modifying the original

    # Iterate through each cell and apply the transformation rules
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            if output_grid[i, j] == 5:
                output_grid[i, j] = 0
            elif output_grid[i, j] == 4:
                output_grid[i, j] = 4 # Redundant, but explicit for clarity.
    return output_grid