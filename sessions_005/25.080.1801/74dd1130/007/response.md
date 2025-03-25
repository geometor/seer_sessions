```python
"""
The transformation transposes the input grid and then swaps the first and last columns of the transposed grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms a 3x3 input grid by transposing it and then swapping the first and last columns.

    Args:
        input_grid: A 3x3 list of lists representing the input grid.

    Returns:
        A 3x3 list of lists representing the transformed grid.
    """
    # Convert the input list of lists to a NumPy array.
    input_array = np.array(input_grid)

    # Transpose the array.
    transposed_array = input_array.T

    # Swap columns 0 and 2 of the transposed array.
    transposed_array[:, [0, 2]] = transposed_array[:, [2, 0]]

    # Convert the NumPy array back to a list of lists.
    output_grid = transposed_array.tolist()

    return output_grid
```