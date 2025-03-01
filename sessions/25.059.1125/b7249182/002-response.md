# b7249182 • 002 • example_3 • investigate_coder

---
```python
"""
Iterates through each pixel of the input grid. If a pixel is non-zero (a seed point),
a cross shape of the same color is created in the output grid, centered on that point.
The cross extends two pixels in each cardinal direction, stopping at grid boundaries.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by creating cross shapes centered on non-zero pixels.

    Args:
        input_grid (list of lists): The input grid represented as a 2D list.

    Returns:
        list of lists: The transformed output grid.
    """
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each pixel
    for i in range(rows):
        for j in range(cols):
            # Identify seed pixels (non-zero)
            if input_grid[i, j] != 0:
                color = input_grid[i, j]
                # Center Cross
                output_grid[i, j] = color

                # Extend Arms (up, down, left, right)
                for k in range(1, 3):  # Extend up to 2 pixels
                    # Up
                    if i - k >= 0:
                        output_grid[i - k, j] = color
                    # Down
                    if i + k < rows:
                        output_grid[i + k, j] = color
                    # Left
                    if j - k >= 0:
                        output_grid[i, j - k] = color
                    # Right
                    if j + k < cols:
                        output_grid[i, j + k] = color

    return output_grid.tolist()
```

