# 1f876c06 • 008 • refine_coder

---
```python
"""
The transformation rule performs a vertical reflection of all non-white pixels across the horizontal midline of the grid. For each non-white pixel in the input grid, a copy of that pixel is placed in the output grid at the vertically mirrored position. The original, non-white, pixel is retained in its original location. White pixels (value 0) are unaffected. The horizontal midline is conceptually located at (height - 1) / 2. The reflected position's row is calculated as `height - 1 - original_row`, and the column remains the same.
"""

import numpy as np

def transform(input_grid):
    """
    Applies a vertical reflection transformation, copying non-white pixels across the horizontal midline.
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
                # Copy the pixel to the reflected position in the output grid.
                output_grid[new_row, col] = input_grid[row, col]

    return output_grid
```
