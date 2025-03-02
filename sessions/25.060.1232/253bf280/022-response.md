# 253bf280 • 022 • example_4 • investigate_coder

---
```python
"""
Find the azure pixels. Keep the azure pixels in the output. Draw a green vertical line between vertically aligned azure pixels.
"""

import numpy as np

def find_pixels_by_color(grid, color):
    """Finds coordinates of all pixels of a specified color."""
    return np.array(np.where(grid == color)).T.tolist()

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find azure pixels
    azure_pixels = find_pixels_by_color(input_grid, 8)

    # Create vertical lines between vertically-aligned azure pixels
    for i in range(len(azure_pixels)):
        for j in range(i + 1, len(azure_pixels)):
            # check if the azure pixels are in the same column
            if azure_pixels[i][1] == azure_pixels[j][1]:
                # draw the green line
                for row in range(min(azure_pixels[i][0], azure_pixels[j][0]) + 1, max(azure_pixels[i][0], azure_pixels[j][0])):
                    output_grid[row, azure_pixels[i][1]] = 3

    return output_grid
```
