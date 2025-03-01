# d13f3404 • 014 • refine_coder

---
```python
"""
The input grid is treated as a 3x3 "core" sub-grid. This core is replicated to construct a 2x2 arrangement of cores. Each time the core is replicated it is rotated 90 degrees clockwise. Arrange these replicated cores to create the final 6x6 grid.
"""

import numpy as np

def rotate_grid(grid):
    """Rotates a grid 90 degrees clockwise."""
    return np.rot90(grid, k=-1)

def transform(input_grid):
    """Transforms the input grid into the output grid by replicating and rotating a 3x3 core."""
    # Convert input to numpy array for easier manipulation
    core = np.array(input_grid)

    # Initialize the output grid as a 6x6 array filled with zeros
    output_grid = np.zeros((6, 6), dtype=int)

    # Place the original core in the top-left corner
    output_grid[:3, :3] = core

    # Rotate and place the core in the top-right corner
    rotated_core = rotate_grid(core)
    output_grid[:3, 3:6] = rotated_core
    
    # Rotate and place the core in the bottom left
    rotated_core = rotate_grid(rotated_core)
    output_grid[3:6, :3] = rotated_core

    # Rotate and place in bottom right
    rotated_core = rotate_grid(rotated_core)
    output_grid[3:6, 3:6] = rotated_core
    
    return output_grid.tolist()
```

