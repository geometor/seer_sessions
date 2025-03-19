# 6fa7a44f • 002 • example_4 • investigate_coder

---
```python
"""
The input grid is duplicated vertically. The order of rows in the duplicated portion is reversed compared to the original.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by duplicating it vertically and reversing the order of rows in the duplicated part.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The transformed output grid.
    """
    # Convert the input grid to a NumPy array for easier manipulation
    input_array = np.array(input_grid)

    # Reverse the rows of the input array
    reversed_array = np.flipud(input_array)

    # Concatenate the original and reversed arrays vertically
    output_array = np.concatenate((input_array, reversed_array), axis=0)

    # Convert the NumPy array back to a list of lists
    output_grid = output_array.tolist()

    return output_grid
```
