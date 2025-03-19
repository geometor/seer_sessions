# cce03e0d • 008 • example_2 • investigate_coder

---
```python
"""
Transforms a 3x3 input grid into a 9x9 output grid by replicating the input in the top-right and bottom-left corners of the output grid, with rotations, and filling the rest with zeros.
"""

import numpy as np

def rotate_90_clockwise(grid):
    return np.rot90(grid, k=-1)

def rotate_270_clockwise(grid):
    return np.rot90(grid, k=1)
    

def transform(input_grid):
    # Initialize a 9x9 output grid filled with zeros.
    output_grid = np.zeros((9, 9), dtype=int)

    # Convert input_grid to numpy array for easier manipulation
    input_grid = np.array(input_grid)
    
    # Top-Right Replication with 90-degree clockwise rotation
    rotated_grid_90 = rotate_90_clockwise(input_grid)
    output_grid[0:3, 6:9] = rotated_grid_90

    # Bottom-Left Replication with 270-degree clockwise rotation
    rotated_grid_270 = rotate_270_clockwise(input_grid)
    output_grid[6:9, 0:3] = rotated_grid_270
    

    return output_grid.tolist()
```
