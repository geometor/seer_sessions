```python
"""
Create an output grid with the same dimensions as the input grid.
For each row in the input grid:
  Read the sequence of pixels in the current row from left to right.
  Reverse the order of this sequence of pixels.
  Place the reversed sequence of pixels into the corresponding row of the output grid.
The resulting grid is the final output.
"""

import numpy as np

def transform(input_grid):
    """
    Reverses the order of pixels in each row of the input grid.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the output grid with each row reversed.
    """
    # Convert input_grid (list of lists) to a numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)

    # Get the dimensions of the input grid
    height, width = input_array.shape

    # Create an output array with the same dimensions, initialized with zeros (or any placeholder)
    # We will fill this completely, so the initial values don't matter.
    output_array = np.zeros((height, width), dtype=int)

    # Iterate through each row index of the input array
    for r in range(height):
        # Get the current row from the input array
        input_row = input_array[r, :]

        # Reverse the sequence of pixels in the current row using slicing
        reversed_row = input_row[::-1]

        # Place the reversed row into the corresponding row of the output array
        output_array[r, :] = reversed_row

    # Convert the output numpy array back to a list of lists, which is the expected format
    output_grid = output_array.tolist()

    return output_grid

```