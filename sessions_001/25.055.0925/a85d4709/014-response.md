# a85d4709 • 014 • example_3 • investigate_coder

---
```python
"""
Replaces gray pixels with red, the center white pixel with yellow, and other white pixels with red.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule:
    - Gray (5) pixels become Red (2).
    - White (0) pixels become Yellow (4) if in the center, otherwise Red (2).

    Args:
        input_grid (numpy.ndarray): The input grid.

    Returns:
        numpy.ndarray: The transformed grid.
    """
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Replace gray (5) with red (2)
    output_grid[output_grid == 5] = 2

    # Check for center pixel and replace white (0) with yellow (4)
    if rows % 2 != 0 and cols % 2 != 0: #check for odd sized grid
        center_row, center_col = rows // 2, cols // 2
        if output_grid[center_row, center_col] == 0:
            output_grid[center_row, center_col] = 4

    # Replace remaining white (0) with red (2)
    output_grid[output_grid == 0] = 2
    
    return output_grid
```
