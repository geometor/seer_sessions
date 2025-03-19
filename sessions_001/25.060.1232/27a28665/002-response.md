# 27a28665 • 002 • example_7 • investigate_coder

---
```python
"""
Counts the number of non-zero (non-white) cells in the input grid and returns a 1x1 grid with the count as its value.
The color of output changes depending on input.
"""

import numpy as np

def transform(input_grid):
    # Convert the input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Count the number of non-zero cells.
    non_zero_count = np.count_nonzero(input_array)
    
    # Create the 1x1 output grid.
    output_grid = np.array([[non_zero_count]])

    return output_grid
```
