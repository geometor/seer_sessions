# a85d4709 • 012 • refine_coder

---
```python
"""
Replaces all pixels in the input grid, which are initially color 8 (azure), with color 3 (green).
The shape and size of the grid remain unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms an input grid of color 8 to an output grid of color 3,
    maintaining the original dimensions.

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

