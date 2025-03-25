```python
"""
Counts the number of non-zero elements that are not part of the central cross in a 3x3 grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms a 3x3 input grid by counting non-zero elements outside the central cross.

    Args:
        input_grid (list of lists): A 3x3 grid of integers.

    Returns:
        int: The count of non-zero elements not on the central cross.
    """
    count = 0
    for i in range(3):
        for j in range(3):
            # Check if the element is non-zero and not part of the central cross
            if input_grid[i][j] != 0 and not (i == 1 or j == 1):
                count += 1
    return count
```