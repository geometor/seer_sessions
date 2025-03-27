```python
"""
Takes a 2D grid (list of lists) as input.
Returns a new 2D grid which is a subgrid of the input, 
excluding the first row and the first column.
"""

import numpy as np

def transform(input_grid):
    """
    Removes the first row and first column from the input grid.

    Args:
        input_grid (list of lists): The input 2D grid.

    Returns:
        list of lists: The output grid with the top row and leftmost column removed.
    """
    # Convert the input list of lists to a numpy array for easier slicing
    input_array = np.array(input_grid, dtype=int)

    # Select the subgrid starting from the second row (index 1) 
    # and the second column (index 1)
    # Slicing input_array[1:] takes all rows from index 1 onwards.
    # Slicing [:, 1:] takes all columns from index 1 onwards from the result.
    output_array = input_array[1:, 1:]

    # Convert the resulting numpy array back to a list of lists
    output_grid = output_array.tolist()

    return output_grid

```