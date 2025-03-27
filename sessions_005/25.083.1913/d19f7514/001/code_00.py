"""
1. Divide Input: Divide the input grid into two equal portions vertically.
2. Discard Bottom: Disregard the bottom half of the input grid completely.
3. Process Top: Focus exclusively on the top half of the input grid.
4. Recolor: Within this top section, replace every instance of the color '3' (green) with the color '4' (yellow).
5. Output: The resulting modified top half becomes the output grid.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the described rule."""

    # Divide the input grid into two equal portions vertically.
    height = input_grid.shape[0]
    midpoint = height // 2
    top_half = input_grid[:midpoint]

    # Create a copy of the top half to modify.  This will be our output.
    output_grid = np.copy(top_half)

    # Recolor: Replace every instance of '3' with '4' in the output grid.
    output_grid[output_grid == 3] = 4

    return output_grid