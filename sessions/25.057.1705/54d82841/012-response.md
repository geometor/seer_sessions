# 54d82841 • 012 • refine_coder

---
```python
"""
Copies the input grid to the output grid. If and only if all pixels in the input grid are white (0), 
then the pixel at the last row and middle column of the output grid is changed to yellow (4).
Otherwise, the output grid is identical to the input grid.
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

    # Check if there are any non-white pixels in the entire grid
    if np.all(input_grid == 0):
        # Find the middle column index
        middle_col = cols // 2
        
        # Change the color of the pixel at the last row and middle column to yellow
        output_grid[-1, middle_col] = 4

    return output_grid
```

