```python
"""
Create an output grid by concatenating the input grid with itself horizontally.
The output grid will have the same height as the input grid but double the width.
The left half of the output grid will be identical to the input grid, and the 
right half will also be identical to the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by duplicating it horizontally.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    # Get the dimensions of the input grid
    # height, width = input_grid.shape

    # Create the output grid by concatenating the input grid with itself along the horizontal axis (axis=1)
    # This effectively places a copy of the input grid to the right of the original.
    output_grid = np.concatenate((input_grid, input_grid), axis=1)

    return output_grid

```