# 760b3cac • 018 • refine_coder

---
```python
"""
Yellow pixels are preserved in their original positions. Azure pixels form a connected region. The bounding box of the azure region becomes filled, changing those pixels to azure.
"""

import numpy as np

def get_bounding_box(grid, color):
    # Find coordinates of the specified color
    pixels = np.argwhere(grid == color)
    
    # If no pixels of the color are found, return None
    if len(pixels) == 0:
        return None
    
    # Find min and max row and col to define the bounding box
    min_row = np.min(pixels[:, 0])
    max_row = np.max(pixels[:, 0])
    min_col = np.min(pixels[:, 1])
    max_col = np.max(pixels[:, 1])
    
    return (min_row, max_row, min_col, max_col)

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)

    # Preserve yellow pixels (they are already in place due to copying)

    # Get bounding box for azure pixels
    azure_bounding_box = get_bounding_box(input_grid, 8)

    # If a bounding box is found, fill it with azure
    if azure_bounding_box:
        min_row, max_row, min_col, max_col = azure_bounding_box
        for row in range(min_row, max_row + 1):
            for col in range(min_col, max_col + 1):
                output_grid[row, col] = 8

    return output_grid
```
