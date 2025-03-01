# a85d4709 • 008 • example_2 • investigate_coder

---
```python
"""
Replaces all cell values in the input grid with the value 3.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by replacing all cell values with 3.

    Args:
        input_grid (list of lists): The input grid represented as a 2D list.

    Returns:
        list of lists: The transformed grid with all values set to 3.
    """
    # Initialize output_grid as a copy of the input_grid, but with same dimensions.
    output_grid = np.full_like(input_grid, 3)
    
    # no need to change because the grid is now filled with '3'
    
    return output_grid.tolist()
```

