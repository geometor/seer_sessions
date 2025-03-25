```python
"""
The input grid is vertically mirrored to create an output grid. The output grid consists of the original input grid stacked on top of a vertically flipped version of the input grid. If the input has odd height, the central row is duplicated in the output at the line of symmetry.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by vertically mirroring it.

    Args:
        input_grid (list of lists): The input grid represented as a 2D list.

    Returns:
        list of lists: The transformed grid.
    """
    input_grid = np.array(input_grid)
    # Reverse the rows of the input grid
    reversed_grid = np.flipud(input_grid)

    # Stack the original and reversed grids vertically
    output_grid = np.vstack((input_grid, reversed_grid))

    return output_grid.tolist()
```