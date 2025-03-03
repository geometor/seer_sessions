# 6150a2bd • 012 • refine_coder

---
```python
"""
The input grid is rotated 90 degrees counter-clockwise to produce the output grid. This means the rows of the input become the columns of the output, and the columns of the input become the rows of the output, but in reverse order. The element at row `r` and column `c` in the input grid will be located at row `c` and column `H-1-r` in the output grid, where `H` is the height of the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Rotates the input grid 90 degrees counter-clockwise.
    """
    # Convert the input grid to a NumPy array.
    input_array = np.array(input_grid)

    # Rotate the array 90 degrees counter-clockwise.
    output_array = np.rot90(input_array)

    # Convert the NumPy array back to a list of lists.
    output_grid = output_array.tolist()

    return output_grid
```

