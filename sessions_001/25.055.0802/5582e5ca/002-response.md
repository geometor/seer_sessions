# 5582e5ca • 002 • example_1 • investigate_coder

---
```python
"""
The transformation rule is to replace all pixels in the input grid with the color yellow (4). The output grid has the same dimensions as the input grid, but every cell is filled with the value 4.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by replacing all pixels with yellow (4).

    Args:
        input_grid (numpy.ndarray): The input grid.

    Returns:
        numpy.ndarray: The output grid with all pixels set to yellow (4).
    """
    # Create a copy of the input grid to serve as the output grid.  We copy to keep the same dimensions.
    output_grid = np.copy(input_grid)

    # Replace all elements in the output_grid with the value 4 (yellow).
    output_grid[:] = 4

    return output_grid
```
