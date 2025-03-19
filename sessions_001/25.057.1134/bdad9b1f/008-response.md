# bdad9b1f • 008 • example_2 • investigate_coder

---
```python
"""
1.  **Azure Object Extension:** The azure (8) object, initially a vertical line of two pixels, extends downwards. The final length of the azure object occupies available space.

2.  **Red Object Expansion and Modification:** The red (2) object, initially a horizontal line of two pixels, expands. A single yellow (4) pixel is inserted into the center of the red object. The red object is then extended to the left and right edges of the grid.

3.  **Background:** Pixels that are not part of the azure or red objects remain white/background (0).
"""

import numpy as np

def find_object(grid, color):
    # Find coordinates of pixels with the specified color.
    coords = np.argwhere(grid == color)
    return coords

def transform(input_grid):
    """Transforms the input grid according to the described rules."""

    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 1. Azure Object Extension
    azure_coords = find_object(input_grid, 8)
    if len(azure_coords) > 0:
        min_azure_row = np.min(azure_coords[:, 0])
        max_azure_col = azure_coords[0][1]
        for row in range(min_azure_row, rows):
            output_grid[row, max_azure_col] = 8

    # 2. Red Object Expansion and Modification
    red_coords = find_object(input_grid, 2)
    if len(red_coords) > 0:
        min_red_row = np.min(red_coords[:, 0])
        max_red_row = np.max(red_coords[:,0])

        # place a yellow (4) pixel in the middle
        output_grid[min_red_row, cols // 2] = 4

        # expand the red object
        for col in range(0, cols):
            output_grid[min_red_row, col] = 2

    return output_grid
```
