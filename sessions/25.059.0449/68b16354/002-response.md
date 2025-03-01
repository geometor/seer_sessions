# 68b16354 • 002 • example_3 • investigate_coder

---
```python
"""
The transformation rule is to reverse the order of the rows in the input grid. The first row becomes the last, the second row becomes the second-to-last, and so on, until the last row becomes the first. The columns are kept the same.

Essentially, the output grid is a vertically flipped version of the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Reverses the order of rows in a given 2D grid.

    Args:
        input_grid: A 2D list or numpy array representing the input grid.

    Returns:
        A 2D list or numpy array with the rows reversed.
    """

    # Convert the input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Reverse the order of rows using array slicing.
    output_array = input_array[::-1]

    # Convert the result back to a list if the input was a list
    if isinstance(input_grid, list):
        output_grid = output_array.tolist()
    else:
        output_grid = output_array

    return output_grid
```
