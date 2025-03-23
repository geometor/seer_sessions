```python
"""
The transformation rule is a one-to-one mapping of digits. To transform the input grid to the output grid, replace each digit in the input with its corresponding mapped value according to the following rules:

*   3 becomes 4
*   1 becomes 5
*   2 becomes 6
*   8 becomes 9
*   5 becomes 1
*   6 becomes 2
*   9 becomes 8
*   4 becomes 3

Essentially, the program performs a direct substitution cipher on the input grid to produce the output grid. Because of identical rows, it applies cipher to first row, then repeats result for other rows.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms an input grid by applying a one-to-one digit mapping.
    """
    # Create a mapping dictionary
    mapping = {
        3: 4,
        1: 5,
        2: 6,
        8: 9,
        5: 1,
        6: 2,
        9: 8,
        4: 3,
    }

    # Initialize the output grid with the same dimensions as the input
    output_grid = np.zeros_like(input_grid)

    # Apply the mapping to each element of the input grid
    for i in range(input_grid.shape[0]):
        for j in range(input_grid.shape[1]):
            output_grid[i, j] = mapping.get(input_grid[i, j], input_grid[i,j]) #default to input if not in the map

    return output_grid
```