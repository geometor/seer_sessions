# 8efcae92 • 020 • refine_coder

---
```python
"""
The transformation identifies the red pixels within the input grid, determines the smallest bounding box 
enclosing those red pixels, expands the bounding box by one cell in each direction, and then reproduces the 
red pixels' relative positions within an output grid with the dimensions of the expanded bounding box. The 
padding pixels added during the expansion are filled with their original values from the input grid.
"""

import numpy as np

def get_red_pixels(grid):
    """Finds the coordinates of all red pixels in the grid."""
    return np.argwhere(grid == 2)

def get_bounding_box(grid, red_pixels):
    """Finds the smallest bounding box containing all red pixels."""
    if len(red_pixels) == 0:
        return 0, -1, 0, -1  # Handle empty case: no red pixels

    min_r, min_c = red_pixels.min(axis=0)
    max_r, max_c = red_pixels.max(axis=0)
    return min_r, max_r, min_c, max_c

def expand_bounding_box(grid, min_r, max_r, min_c, max_c):
    """Expands the bounding box by one cell in all directions, with bounds checking"""
    min_r = max(0, min_r - 1)
    max_r = min(grid.shape[0] - 1, max_r + 1)
    min_c = max(0, min_c - 1)
    max_c = min(grid.shape[1] - 1, max_c + 1)
    return min_r, max_r, min_c, max_c
    

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # 1. Identify Red Pixels
    red_pixels = get_red_pixels(input_grid)

    # 2. Find Minimum Bounding Box
    min_r, max_r, min_c, max_c = get_bounding_box(input_grid, red_pixels)

    # 3. Expand the bounding box
    min_r_exp, max_r_exp, min_c_exp, max_c_exp = expand_bounding_box(input_grid, min_r, max_r, min_c, max_c)
    
    # 4. Create Output Grid based on expanded bounding box
    output_grid = np.zeros((max_r_exp - min_r_exp + 1, max_c_exp - min_c_exp + 1), dtype=int)

    # 5. Populate output grid
    for r in range(min_r_exp, max_r_exp + 1):
        for c in range(min_c_exp, max_c_exp + 1):
            output_grid[r - min_r_exp, c - min_c_exp] = input_grid[r,c]

    return output_grid.tolist()
```
