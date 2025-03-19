# 1f876c06 • 004 • example_1 • investigate_coder

---
```python
"""
The transformation rule is a vertical reflection (mirroring) of non-white pixels. Non-white pixels in the input grid are repositioned in the output grid such that their horizontal position remains the same, but their vertical position is mirrored across the horizontal midline of the grid. White pixels remain unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Applies a vertical reflection transformation to non-white pixels in the input grid.
    """
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    height = output_grid.shape[0]

    # Iterate through the input grid to find non-white pixels.
    for row in range(height):
        for col in range(output_grid.shape[1]):
            if input_grid[row, col] != 0:
                # Calculate the new row index for vertical reflection.
                new_row = height - 1 - row
                # Update the output grid with the reflected pixel.
                output_grid[new_row, col] = input_grid[row, col]
                # clear the old position by setting to zero
                if (new_row != row):
                  output_grid[row,col] = 0

    return output_grid
```
