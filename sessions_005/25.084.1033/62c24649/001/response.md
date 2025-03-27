```python
"""
Create a larger grid by tiling the input grid and its reflections.
The output grid's dimensions are double the input grid's dimensions (2*H x 2*W).
The output grid is composed of four quadrants:
- Top-left: The original input grid.
- Top-right: The input grid flipped horizontally.
- Bottom-left: The input grid flipped vertically.
- Bottom-right: The input grid flipped both horizontally and vertically.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by creating a 2x2 tiled grid composed of
    the original grid and its horizontal, vertical, and combined reflections.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists of integers.

    Returns:
        numpy.ndarray: The transformed grid as a NumPy array.
    """
    # Convert input list of lists to a NumPy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)

    # Get the dimensions of the input grid
    H, W = input_np.shape

    # Create the reflected versions of the input grid
    # I_hflip: Flip horizontally (left-right)
    hflip = np.fliplr(input_np)
    # I_vflip: Flip vertically (up-down)
    vflip = np.flipud(input_np)
    # I_vhflip: Flip both horizontally and vertically
    vhflip = np.flipud(np.fliplr(input_np)) # or np.fliplr(np.flipud(input_np))

    # Initialize the output grid with doubled dimensions
    output_H, output_W = 2 * H, 2 * W
    output_grid = np.zeros((output_H, output_W), dtype=int)

    # Place the original and reflected grids into the corresponding quadrants
    # Top-left quadrant: Original input grid
    output_grid[0:H, 0:W] = input_np
    # Top-right quadrant: Horizontally flipped grid
    output_grid[0:H, W:output_W] = hflip
    # Bottom-left quadrant: Vertically flipped grid
    output_grid[H:output_H, 0:W] = vflip
    # Bottom-right quadrant: Both horizontally and vertically flipped grid
    output_grid[H:output_H, W:output_W] = vhflip

    return output_grid

```