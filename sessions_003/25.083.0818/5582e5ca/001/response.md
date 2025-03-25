```python
"""
The transformation rule identifies the top-right element of the input grid and uses its value to populate a new 3x3 grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms a 3x3 input grid into a 3x3 output grid where all cells
    have the value of the top-right element of the input grid.
    """
    # Identify the top-right element in the input grid.
    top_right_element = input_grid[0, -1]

    # Create the output grid and populate it with the top-right element's value.
    output_grid = np.full((3, 3), top_right_element)

    return output_grid
```