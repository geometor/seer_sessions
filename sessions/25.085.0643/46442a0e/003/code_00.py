"""
Creates an output grid that is twice the height and width of the input grid.
The output grid is composed of four quadrants, each containing a rotated version of the input grid:
1. Top-left: The original input grid (0 degrees rotation).
2. Top-right: The input grid rotated 90 degrees clockwise.
3. Bottom-left: The input grid rotated 90 degrees counter-clockwise (270 degrees clockwise).
4. Bottom-right: The input grid rotated 180 degrees.
"""

import numpy as np

def transform(input_grid):
    """
    Applies the rotation and tiling transformation to the input grid.

    Args:
        input_grid (list of list of int): The input grid.

    Returns:
        list of list of int: The transformed output grid.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)

    # Determine the height (H) and width (W) of the input grid
    # Note: NumPy's shape is (rows, columns), corresponding to (height, width)
    H, W = input_np.shape

    # Calculate the dimensions of the output grid (2H x 2W)
    output_H, output_W = 2 * H, 2 * W

    # Create an empty output grid with the calculated dimensions, filled with a default color (e.g., 0)
    # Ensure the dtype matches the input to handle color values correctly
    output_grid = np.zeros((output_H, output_W), dtype=int)

    # 1. Top-left quadrant: Copy the original input grid (0 degrees rotation)
    output_grid[0:H, 0:W] = input_np

    # 2. Top-right quadrant: Rotate 90 degrees clockwise (k=-1 or k=3)
    rotated_90_cw = np.rot90(input_np, k=-1)
    output_grid[0:H, W:output_W] = rotated_90_cw

    # 3. Bottom-left quadrant: Rotate 90 degrees counter-clockwise (k=1)
    rotated_90_ccw = np.rot90(input_np, k=1)
    output_grid[H:output_H, 0:W] = rotated_90_ccw

    # 4. Bottom-right quadrant: Rotate 180 degrees (k=2 or k=-2)
    rotated_180 = np.rot90(input_np, k=2)
    output_grid[H:output_H, W:output_W] = rotated_180

    # Convert the final numpy array back to a list of lists before returning
    return output_grid.tolist()
