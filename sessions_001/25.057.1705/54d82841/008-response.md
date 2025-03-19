# 54d82841 • 008 • example_2 • investigate_coder

---
```python
"""
Copies the input grid to the output grid, then changes the color of the pixel at the last row and middle column to yellow (4) if there aren't any non-white colored at the bottom.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the specified rule.
    
    Args:
        input_grid (numpy.ndarray): The input grid.
    
    Returns:
        numpy.ndarray: The transformed grid.
    """
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Check if there are any non-white pixels in the last row
    last_row = output_grid[-1, :]
    if np.all(last_row == 0):
      # Find the middle column index
      middle_col = cols // 2
      
      # Change the color of the pixel at the last row and middle column to yellow
      output_grid[-1, middle_col] = 4

    return output_grid
```
