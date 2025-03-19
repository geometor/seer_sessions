# d9fac9be • 012 • example_3 • investigate_coder

---
```python
"""
Counts the number of blue pixels in the input grid and returns 1 if blue is present, otherwise 0.
"""

import numpy as np

def transform(input_grid):
    """
    Counts occurrences of each color and returns the 'blue' color code (1) if blue exists in the grid.
    """
    # Convert input_grid to a NumPy array for easier manipulation
    grid = np.array(input_grid)

    # Count the occurrences of blue (1) pixels.
    blue_count = np.count_nonzero(grid == 1)
    
    # Determine output based on blue color
    if (blue_count > 0):
      output_grid = np.array([[1]])
    else:
      output_grid = np.array([[0]])

    return output_grid
```
