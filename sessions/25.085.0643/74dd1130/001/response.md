```python
"""
Takes an input grid and transposes it, meaning the rows of the input grid become
the columns of the output grid, and the columns of the input grid become the
rows of the output grid. The element at input[row][col] moves to output[col][row].
"""

import numpy as np

def transform(input_grid):
    """
    Transposes the input grid.

    Args:
        input_grid (list of list of int): The input 2D grid.

    Returns:
        list of list of int: The transposed grid.
    """
    # Convert the input list of lists to a NumPy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)

    # Perform the transpose operation using NumPy's .T attribute
    # This swaps the rows and columns: input_array[i, j] becomes output_array[j, i]
    output_array = input_array.T

    # Convert the resulting NumPy array back to a list of lists
    output_grid = output_array.tolist()

    return output_grid

```