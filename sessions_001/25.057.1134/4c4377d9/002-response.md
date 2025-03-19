# 4c4377d9 • 002 • example_1 • investigate_coder

---
```python
"""
The transformation rule is a vertical replication of the input grid. The input grid is duplicated and placed below the original.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by vertically replicating it.

    Args:
        input_grid (list of lists): The input grid represented as a 2D list.

    Returns:
        list of lists: The transformed grid, which is the input grid replicated vertically.
    """
    # Convert the input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Replicate the input array vertically once.
    output_array = np.concatenate((input_array, input_array), axis=0)

    # Convert the NumPy array back to a list of lists.
    output_grid = output_array.tolist()

    return output_grid
```

