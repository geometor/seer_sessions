# c1d99e64 • 016 • example_3 • investigate_coder

---
```python
"""
The transformation changes white pixels to red if they are directly adjacent to a green pixel.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by changing white (0) pixels to red (2)
    if they are adjacent to a green (3) pixel.
    """
    # Create a copy of the input grid to modify.  Use numpy for easier handling.
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Iterate through each pixel of the grid.
    for i in range(rows):
        for j in range(cols):
            # Check if the current pixel is white (0).
            if output_grid[i, j] == 0:
                # Check neighbors (up, down, left, right).
                neighbors = []
                if i > 0:
                    neighbors.append(output_grid[i - 1, j])  # Up
                if i < rows - 1:
                    neighbors.append(output_grid[i + 1, j])  # Down
                if j > 0:
                    neighbors.append(output_grid[i, j - 1])  # Left
                if j < cols - 1:
                    neighbors.append(output_grid[i, j + 1])  # Right

                # If any neighbor is green (3), change the pixel to red (2).
                if 3 in neighbors:
                    output_grid[i, j] = 2

    return output_grid
```
