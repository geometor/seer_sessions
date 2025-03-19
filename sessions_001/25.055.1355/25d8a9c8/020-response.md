# 25d8a9c8 • 020 • example_4 • investigate_coder

---
```python
"""
The transformation identifies the bottom row of the input grid. It replaces
the corresponding row in the output grid with gray (5) and fills the rest of the
output grid with white (0).
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on the color of pixels in the bottom row.
    
    Args:
        input_grid: A 2D numpy array representing the input grid.
        
    Returns:
        A 2D numpy array representing the transformed output grid.
    """
    # Initialize the output grid with the same dimensions as the input grid, filled with white (0).
    output_grid = np.zeros_like(input_grid)
    
    # Get the height of the grid.
    height = input_grid.shape[0]
    
    # Replace the bottom row of the output grid with gray (5).
    output_grid[height - 1, :] = 5

    return output_grid
```
