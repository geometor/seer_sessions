```python
"""
The transformation extracts the top-rightmost 3x3 subgrid of non-zero elements from the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Extracts the 3x3 subgrid from the top right corner of non zero values.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The extracted 3x3 subgrid.
    """
    # Convert input_grid to numpy array for easier manipulation
    input_array = np.array(input_grid)
    rows, cols = input_array.shape

    # Find the indices of non-zero elements
    non_zero_indices = np.argwhere(input_array != 0)

    # Find the top-rightmost non-zero row and column
    if non_zero_indices.size > 0:
      top_most_row = 0
      right_most_col = 0

      for r in range(rows):
        for c in range(cols):
          if input_array[r][c] != 0:
            top_most_row = r
            break
        else:
          continue
        break

      for c in range(cols-1,-1,-1):
        for r in range(rows):
          if input_array[r][c] != 0:
            right_most_col = c
            break
        else:
          continue
        break

      output_array = input_array[top_most_row:top_most_row+3, right_most_col-2:right_most_col+1]

    else:
      output_array = np.zeros((3,3))

    return output_array.tolist()
```