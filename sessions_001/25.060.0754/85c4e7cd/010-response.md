# 85c4e7cd • 010 • example_2 • investigate_coder

---
```python
"""
Swap all pixels of color 2 (red) with color 6 (magenta) and vice-versa.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by swapping colors 2 and 6.
    
    Args:
        input_grid (numpy.ndarray): The input grid.
        
    Returns:
        numpy.ndarray: The transformed grid.
    """
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Swap color 2 with color 6 and vice versa.
    output_grid[input_grid == 2] = 6
    output_grid[input_grid == 6] = 2

    return output_grid
```
