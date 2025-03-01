# 5bd6f4ac • 008 • example_2 • investigate_coder

---
```python
"""
The transformation extracts the bottom-right 3x3 subgrid from the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Extracts the bottom-right 3x3 subgrid from the input grid.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The bottom-right 3x3 subgrid.
    """
    # Convert input grid to numpy array for easier slicing
    input_array = np.array(input_grid)

    # Get the dimensions of the input grid
    rows, cols = input_array.shape

    # Extract the bottom-right 3x3 subgrid
    output_array = input_array[rows-3:, cols-3:]

    # Convert the numpy array back to a list of lists
    output_grid = output_array.tolist()

    return output_grid
```
