# 794b24be • 002 • example_10 • investigate_coder

---
```python
"""
Replaces all blue pixels (1) in the input grid with red pixels (2), keeping the white pixels (0) unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by replacing blue pixels with red pixels.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the output grid.
    """
    # Create a copy of the input grid to serve as the output grid.
    output_grid = np.copy(input_grid)
    
    # Iterate through each cell of the input grid.
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            # If the cell is blue (1), change it to red (2).
            if output_grid[i, j] == 1:
                output_grid[i, j] = 2

    return output_grid
```
