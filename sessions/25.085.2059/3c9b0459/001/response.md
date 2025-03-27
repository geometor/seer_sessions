```python
"""
Rotates the input grid by 180 degrees.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by rotating it 180 degrees.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the 180-degree rotated output grid.
    """
    # Convert the input list of lists to a numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)

    # Get the dimensions (height H, width W) of the input grid
    H, W = input_np.shape

    # Create a new numpy array of the same dimensions to store the output
    # Initialize with zeros or any placeholder value
    output_np = np.zeros_like(input_np)

    # Iterate through each pixel in the input grid
    for r in range(H):
        for c in range(W):
            # Calculate the target position in the output grid for 180-degree rotation
            # Target row is H - 1 - r
            # Target column is W - 1 - c
            r_out = H - 1 - r
            c_out = W - 1 - c

            # Copy the color value from the input pixel to the target position in the output grid
            output_np[r_out, c_out] = input_np[r, c]

    # Convert the output numpy array back to a list of lists before returning
    output_grid = output_np.tolist()

    return output_grid

```