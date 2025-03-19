# 6150a2bd • 008 • example_2 • investigate_coder

---
```python
"""
The transformation rule is a 180-degree rotation of the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Rotates the input grid by 180 degrees.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the rotated grid.
    """
    # Initialize the output grid as a copy of the input grid.  Not strictly necessary
    # for this simple rotation, but good practice for more complex transformations.
    output_grid = np.copy(input_grid)

    # Rotate the grid by 180 degrees.  Could also use np.rot90(input_grid, 2)
    output_grid = np.flip(np.flip(output_grid, 0), 1)
    
    return output_grid
```
