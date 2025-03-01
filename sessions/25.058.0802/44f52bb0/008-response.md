# 44f52bb0 • 008 • example_2 • investigate_coder

---
```python
"""
Counts the number of red (value 2) pixels in the input grid, adds 4 to the count, and returns the result as a 1x1 grid.
"""

import numpy as np

def transform(input_grid):
    # Count the number of red pixels (value 2).
    red_pixel_count = np.count_nonzero(input_grid == 2)

    # Add 4 to the count of red pixels
    output_value = red_pixel_count + 4
    
    #initialize a 1x1 grid,
    output_grid = np.array([[output_value]])

    return output_grid
```
