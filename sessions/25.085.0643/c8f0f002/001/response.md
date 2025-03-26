```python
"""
Iterate through each pixel of the input grid. If a pixel's color is orange (7), change its color to gray (5) in the output grid. All other pixels retain their original color. The output grid has the same dimensions as the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by changing all orange (7) pixels to gray (5).

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    # Get the dimensions of the input grid
    height = len(input_grid)
    width = len(input_grid[0])

    # Create a copy of the input grid to modify, ensuring the original is unchanged
    # and pixels not matching the condition are preserved.
    output_grid = np.copy(input_grid)

    # Iterate through each pixel of the grid
    for r in range(height):
        for c in range(width):
            # Check if the pixel color is orange (7)
            if input_grid[r][c] == 7:
                # Change the corresponding pixel in the output grid to gray (5)
                output_grid[r][c] = 5
            # No else needed because we started with a copy, so other pixels already have the correct color.

    return output_grid

```