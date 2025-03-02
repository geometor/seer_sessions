# 44f52bb0 • 018 • example_4 • investigate_coder

---
```python
"""
Counts the number of red pixels (value 2) in the input grid and returns the count.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid to output.

    Args:
        input_grid (list of lists): A 2D array representing the input grid.

    Returns:
        int: single integer count of the number of occurances of 2 in the
        input_grid.
    """
    # Convert the input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Count the number of pixels with value 2 (red pixels).
    count = np.count_nonzero(input_array == 2)

    return count
```
