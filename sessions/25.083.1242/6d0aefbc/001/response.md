```python
"""
The transformation rule is: Duplicate each column of the input grid to its right, resulting in an output grid with double the width.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by duplicating each of its columns.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The transformed grid with duplicated columns.
    """
    input_grid = np.array(input_grid)
    output_grid = []

    # Iterate through each column of the input grid.
    for col in range(input_grid.shape[1]):
        # Duplicate the current column and append it to the output grid.
        output_grid.append(input_grid[:, col])
        output_grid.append(input_grid[:, col])  # Duplicate

    return np.array(output_grid).transpose().tolist()
```