# 27a28665 • 020 • example_4 • investigate_coder

---
```python
"""
Counts the number of blue pixels (represented by the value 1) in the input grid and returns the count as a single-element grid.
"""

import numpy as np

def transform(input_grid):
    """
    Counts the occurrences of the color blue (represented by 1) in the input grid.

    Args:
        input_grid (list of lists): A 2D array representing the input grid.

    Returns:
        int: The count of blue pixels.
    """
    # Convert the input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Count the number of blue pixels (value 1).
    blue_count = np.count_nonzero(input_array == 1)

    # return the count
    return blue_count
```
