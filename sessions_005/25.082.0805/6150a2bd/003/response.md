```python
"""
The transformation rearranges the rows of the input grid to form the output grid.
The last row of the input becomes the first row of the output.
The first row of the input becomes the last row of the output.
The middle row of the input is reversed to form the middle row of the output.
"""

import numpy as np

def reverse_row(row):
    """Reverses the order of elements in a row."""
    return row[::-1]

def transform(input_grid):
    # Convert input grid to a NumPy array
    input_array = np.array(input_grid)
    
    # Get the number of rows
    num_rows = input_array.shape[0]

    # Initialize the output grid
    output_array = np.empty_like(input_array)

    # Last row of input becomes the first row of output
    output_array[0, :] = input_array[num_rows - 1, :]

    # First row of input becomes the last row of output
    output_array[num_rows - 1, :] = input_array[0, :]

    # Reverse the middle row
    if num_rows > 2:
      output_array[1,:] = reverse_row(input_array[1,:])

    # Convert the NumPy array back to a list of lists
    output_grid = output_array.tolist()
    return output_grid
```