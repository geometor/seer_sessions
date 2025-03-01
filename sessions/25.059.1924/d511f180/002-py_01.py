"""
The transformation rule is as follows:
1. Iterate through each pixel in the input grid.
2. For each pixel:
    - If the pixel's color is 5 (gray), and color 8 (azure) is anywhere in the input, replace it with 8 (azure).
    - If the pixel's color is 8 (azure), and color 5 (gray) is anywhere in the input, replace it with 5 (gray).
3. All other pixels retain their original color.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the specified rule.
    """
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Check if both 5 and 8 exist in the input grid.
    has_5 = 5 in input_grid
    has_8 = 8 in input_grid

    # Iterate through each pixel and apply the transformation.
    for r in range(rows):
        for c in range(cols):
            if has_5 and has_8:
                if input_grid[r, c] == 5:
                    output_grid[r, c] = 8
                elif input_grid[r, c] == 8:
                    output_grid[r, c] = 5
            #else, leave as is

    return output_grid