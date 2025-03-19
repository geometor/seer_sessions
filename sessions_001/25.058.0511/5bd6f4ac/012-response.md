# 5bd6f4ac • 012 • refine_coder

---
```python
"""
The transformation extracts the bottom-right 3x3 subgrid from the input grid,
regardless of the input grid's size. The subgrid will always contain the
bottom-right corner pixel, and extends upwards and leftwards to create a 3x3
square. If the input grid has fewer than 3 rows or columns, the behavior is
equivalent to padding the input grid with zeros *above* and *to the left* until
it becomes at least 3x3, and then extracting the bottom-right 3x3 subgrid.
"""

import numpy as np

def transform(input_grid):
    """
    Extracts the bottom-right 3x3 subgrid from the input grid.  If the input
    grid has fewer than 3 rows or columns, it effectively takes as much of
    the bottom-right corner as possible to construct a 3x3 grid filled mostly
    with 0, but with the values of the bottom right corner of the input grid.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The bottom-right 3x3 subgrid.
    """
    # Convert input grid to numpy array for easier slicing
    input_array = np.array(input_grid)

    # Get the dimensions of the input grid
    rows, cols = input_array.shape

    # Initialize a 3x3 output array filled with zeros
    output_array = np.zeros((3, 3), dtype=int)

    # Calculate the starting row and column indices for slicing
    start_row = max(0, rows - 3)
    start_col = max(0, cols - 3)

    # Extract the relevant portion of the input array
    subgrid = input_array[start_row:, start_col:]

    # Calculate where to place the subgrid in output array
    output_row_start = 3 - subgrid.shape[0]
    output_col_start = 3 - subgrid.shape[1]

    # Place the subgrid into the output array
    output_array[output_row_start:, output_col_start:] = subgrid
    
    # Convert the numpy array back to a list of lists
    output_grid = output_array.tolist()

    return output_grid
```

