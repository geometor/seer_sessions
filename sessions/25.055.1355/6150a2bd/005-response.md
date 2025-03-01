# 6150a2bd • 005 • refine_coder

---
```python
"""
The input grid is transformed into the output grid by rotating it by -90 degrees.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by rotating it -90 degrees.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert the input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # 1. Invert Rows: Reverse the order of rows.
    inverted_array = np.flipud(input_array)

    # 2. Transpose: Swap rows and columns.
    output_array = inverted_array.transpose()

    # Convert the NumPy array back to a list of lists.
    output_grid = output_array.tolist()

    return output_grid
```

