```python
"""
The transformation is a 180-degree rotation of the input grid. This can also be achieved by transposing the matrix and then reversing the order of the rows.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by rotating it 180 degrees.

    Args:
        input_grid: A 2D list representing the input grid.

    Returns:
        A 2D list representing the rotated output grid.
    """
    # Convert the input list to a NumPy array
    input_array = np.array(input_grid)

    # Transpose the array
    transposed_array = input_array.T

    # Reverse the order of rows
    rotated_array = transposed_array[::-1]

    # Convert the NumPy array back to a list
    output_grid = rotated_array.tolist()

    return output_grid
```
