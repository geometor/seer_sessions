# 25d8a9c8 • 002 • example_1 • investigate_coder

---
```python
"""
The transformation rule is a simple color substitution. Each pixel in the input grid is replaced with a new color in the output grid based on the following mapping:

1.  Yellow (4) pixels in the input become Gray (5) pixels in the output.
2.  Red (2) pixels in the input become White (0) pixels in the output.
3.  Green (3) pixels in the input become White (0) pixels in the output.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms an input grid by applying a color mapping.
    """
    # initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # Apply color mapping
    output_grid[input_grid == 4] = 5  # Yellow becomes Gray
    output_grid[input_grid == 2] = 0  # Red becomes White
    output_grid[input_grid == 3] = 0  # Green becomes White

    return output_grid
```

