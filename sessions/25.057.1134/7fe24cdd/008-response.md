# 7fe24cdd • 008 • example_2 • investigate_coder

---
```python
"""
The output grid is a 2x2 arrangement of the input grid, where each quadrant is a reflected version of the input:

1. Top-Left Quadrant: Identical to the input grid.
2. Top-Right Quadrant: Horizontally reflected copy of the input grid.
3. Bottom-Left Quadrant: Vertically reflected copy of the input grid.
4. Bottom-Right Quadrant: Horizontally and vertically reflected (180-degree rotated) copy of the input grid.
"""

import numpy as np

def reflect_horizontal(grid):
    return np.fliplr(grid)

def reflect_vertical(grid):
    return np.flipud(grid)

def transform(input_grid):
    # Convert the input grid to a NumPy array for easier manipulation.
    input_np = np.array(input_grid)
    
    # Get dimensions of the input grid.
    rows, cols = input_np.shape
    
    # Initialize the output grid with double the dimensions of the input grid.
    output_grid = np.zeros((rows * 2, cols * 2), dtype=int)
    
    # Top-Left Quadrant: Copy the input grid as is.
    output_grid[:rows, :cols] = input_np
    
    # Top-Right Quadrant: Horizontally reflected copy.
    output_grid[:rows, cols:] = reflect_horizontal(input_np)
    
    # Bottom-Left Quadrant: Vertically reflected copy.
    output_grid[rows:, :cols] = reflect_vertical(input_np)
    
    # Bottom-Right Quadrant: Horizontally and vertically reflected copy.
    output_grid[rows:, cols:] = reflect_horizontal(reflect_vertical(input_np))
    
    return output_grid.tolist()
```
