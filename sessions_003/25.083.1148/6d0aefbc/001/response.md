```python
"""
The transformation rule is to duplicate each column of the input grid and place it to its right.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by duplicating each column.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed grid.
    """
    # Convert the input list of lists to a NumPy array.  Makes processing easier.
    input_grid = np.array(input_grid)

    # Get the number of rows and columns of the input grid.
    rows, cols = input_grid.shape

    # Initialize the output grid with twice the width.  Use zeros for initial values.
    output_grid = np.zeros((rows, cols * 2), dtype=int)

    # Iterate through the columns of the input grid.
    for j in range(cols):
        # Copy the current column from input to the output grid, at positions 2j and 2j+1
        output_grid[:, 2 * j] = input_grid[:, j]
        output_grid[:, 2 * j + 1] = input_grid[:, j]

    return output_grid.tolist() # Convert back to list for consistency with input type
```