# a740d043 • 018 • refine_coder

---
```python
"""
Locate the single orange pixel (color 7) within the input grid.  Extract a 2x2
block from the input grid such that the orange pixel is in the top-left corner
of the block. This 2x2 block is the output grid.
"""

import numpy as np

def find_orange_pixel(grid):
    """Finds the coordinates of the orange pixel (color 7)."""
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 7:
                return (r, c)
    return None

def transform(input_grid):
    """Extracts the 2x2 block with the orange pixel at the top-left."""
    
    # Convert input to numpy array for easier manipulation
    input_grid = np.array(input_grid)

    # Find the coordinates of the orange pixel
    orange_pixel_coords = find_orange_pixel(input_grid)

    # Extract the 2x2 block if the orange pixel is found
    if orange_pixel_coords:
        r, c = orange_pixel_coords
        output_grid = input_grid[r:r+2, c:c+2]
    else:
        output_grid = np.array([])  # Default: empty grid if no orange pixel

    return output_grid.tolist()
```
