```python
"""
Iterate through each pixel of the input grid. If a pixel has a non-zero neighbor to its immediate left, and the neighbor's color is different from the current pixel's color, change the pixel's color to match the neighbor's color.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by replacing the color of a pixel with the color of its left neighbor if it's non-zero and of a different color.
    """
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Iterate through each pixel
    for row in range(rows):
        for col in range(cols):
            # Check the pixel to the immediate left
            if col > 0:  # Ensure there's a pixel to the left
                left_neighbor = output_grid[row, col - 1]
                if left_neighbor != 0:  # Check if the left neighbor is not black
                    # Check if the colors are different.
                    if left_neighbor != output_grid[row,col]:
                        # Replace the current pixel's color with the left neighbor's color
                        output_grid[row, col] = left_neighbor

    return output_grid
```
