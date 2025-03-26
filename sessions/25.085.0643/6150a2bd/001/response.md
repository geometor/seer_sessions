```python
"""
Rotates the input grid by 180 degrees around its center.

1. Determine the dimensions (height and width) of the input grid.
2. Create a new output grid with the same dimensions as the input grid, initialized with zeros (white).
3. For each pixel in the input grid located at coordinates (row, column):
    a. Calculate the target coordinates in the output grid as (height - 1 - row, width - 1 - column).
    b. Copy the color of the input pixel at (row, column) to the target coordinates in the output grid.
4. Return the completed output grid.

Alternatively, use numpy's built-in rotation function for a 180-degree rotation (k=2).
"""

import numpy as np

def transform(input_grid):
    """
    Rotates the input grid by 180 degrees.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the 180-degree rotated grid.
    """
    # Convert input list of lists to a numpy array for efficient rotation
    input_array = np.array(input_grid, dtype=int)

    # Perform a 180-degree rotation.
    # np.rot90 rotates counter-clockwise. Rotating twice (k=2) achieves 180 degrees.
    output_array = np.rot90(input_array, k=2)

    # Convert the resulting numpy array back to a list of lists format
    output_grid = output_array.tolist()

    return output_grid

```