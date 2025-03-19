# ea786f4a • 002 • example_1 • investigate_coder

---
```python
"""
Changes the corner pixels of the input grid to white (0).
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by changing the color of the corner pixels to white (0).
    
    Args:
        input_grid (numpy.ndarray): The input grid.
    
    Returns:
        numpy.ndarray: The transformed grid.
    """
    # Initialize the output grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    
    # Get the dimensions of the grid
    rows, cols = output_grid.shape
    
    # Change the color of the corner pixels to white (0)
    output_grid[0, 0] = 0
    output_grid[0, cols - 1] = 0
    output_grid[rows - 1, 0] = 0
    output_grid[rows - 1, cols - 1] = 0
    
    return output_grid
```
