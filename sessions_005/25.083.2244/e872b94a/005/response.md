```python
"""
Creates a single-column output grid filled with black (0) pixels, where the height of the output grid is equal to the height of the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid into an output grid based on the input grid's height.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the output grid.
    """
    # Determine the number of rows in the input grid.
    num_rows = input_grid.shape[0]

    # Create an output grid that is a single column with a height equal to the number of rows in the input grid.
    output_grid = np.zeros((num_rows, 1), dtype=int)

    # Fill all cells of the output grid with black (0). (Already done by np.zeros)

    return output_grid
```
