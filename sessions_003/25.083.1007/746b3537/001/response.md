```python
"""
The transformation rule extracts one instance of each row from the input grid and stacks them to create the output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by extracting one instance of each row.

    Args:
        input_grid (list of lists): The input grid represented as a 2D list.

    Returns:
        list of lists: The transformed output grid.
    """
    # initialize output_grid
    output_grid = []

    # Iterate through the rows of the input grid.
    for row in input_grid:
        # Check if the row exists before.
        if row not in output_grid:
          # Construct output grid.
          output_grid.append(row)

    return output_grid
```