# ded97339 • 014 • refine_coder

---
```python
"""
1.  **Locate Azure Pixels:** Find the x-coordinate of all azure (8) pixels in the input grid.
2.  **Draw Vertical Lines:**  For each azure pixel, draw a vertical line of azure pixels across the entire height of the grid. The x-coordinate of each vertical line is the same as the x-coordinate of its corresponding azure pixel.
3. **Fill with White**: Set all other pixels in the grid to white (0).
"""

import numpy as np

def find_azure_pixels(grid):
    # Find coordinates of all azure (8) pixels
    return np.argwhere(grid == 8)

def transform(input_grid):
    """Transforms the input grid according to the observed rule."""
    output_grid = np.zeros_like(input_grid)  # Initialize with white (0)
    azure_pixels = find_azure_pixels(input_grid)

    # Vertical Propagation
    for x, y in azure_pixels:
        for i in range(output_grid.shape[0]):
            output_grid[i, x] = 8

    return output_grid
```
