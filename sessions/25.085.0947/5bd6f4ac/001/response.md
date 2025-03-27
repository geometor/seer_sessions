```python
"""
The transformation rule is to extract a specific 3x3 subgrid from the input grid.
This subgrid is located at the top-right corner of the input grid, specifically
spanning rows 0, 1, and 2, and columns 6, 7, and 8. The output grid is an
exact copy of this extracted subgrid.
"""

import numpy as np

def transform(input_grid):
    """
    Extracts the 3x3 subgrid from the top-right corner of the input grid.

    Args:
        input_grid (list of list of int): The input grid.

    Returns:
        list of list of int: The extracted 3x3 subgrid.
    """
    # Convert the input list of lists to a NumPy array for easier slicing
    input_array = np.array(input_grid)

    # Define the boundaries for the subgrid extraction
    start_row = 0
    end_row = 3  # Exclusive index for slicing (0, 1, 2)
    start_col = 6
    end_col = 9  # Exclusive index for slicing (6, 7, 8)

    # Extract the 3x3 subgrid using array slicing
    output_array = input_array[start_row:end_row, start_col:end_col]

    # Convert the NumPy array back to a list of lists for the expected output format
    output_grid = output_array.tolist()

    return output_grid
```