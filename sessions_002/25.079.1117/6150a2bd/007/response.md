```python
"""
The input grid is transformed by transposing it, reversing the order of elements within each row, and then swapping the first and last columns.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by transposing, reversing each row, and swapping the first and last columns.
    """
    # Convert the input grid to a NumPy array.
    input_array = np.array(input_grid)

    # Transpose the array.
    transposed_array = input_array.T

    # Reverse the order of elements in each row.
    reversed_array = np.fliplr(transposed_array)
    
    # Convert to list to swap columns
    output_array = reversed_array.tolist()

    # Swap the first and last columns, if there is more than 1 column.
    if len(output_array) > 0 and len(output_array[0]) > 1:
      for row in output_array:
        row[0], row[-1] = row[-1], row[0]


    # Convert the NumPy array back to a list of lists.
    output_grid = output_array

    return output_grid
```