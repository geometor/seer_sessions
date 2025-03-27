```python
"""
Creates a single-column output grid filled with black (0) pixels, where the height of the output grid is determined by the height of the corresponding output example.
"""

import numpy as np

def transform(input_grid, output_grid_example):
    """
    Transforms the input grid into an output grid based on the height of the example output.

    Args:
        input_grid: A 2D numpy array representing the input grid.
        output_grid_example: A 2D numpy array representing the example output grid, used to determine the output size.

    Returns:
        A 2D numpy array representing the output grid.
    """
    # Determine the number of rows in the output grid example.
    num_rows = output_grid_example.shape[0]

    # Create an output grid that is a single column with a height equal to the number of rows in the example output.
    output_grid = np.zeros((num_rows, 1), dtype=int)

    # Fill all cells of the output grid with black (0).  (Already done by np.zeros)

    return output_grid
```
