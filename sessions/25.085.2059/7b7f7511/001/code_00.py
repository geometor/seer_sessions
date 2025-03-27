"""
Determines the transformation rule for an input grid based on its dimensions.

1. Get the height (H) and width (W) of the input grid.
2. Compare W and H.
3. If W > H, the output grid is the left half of the input grid (columns 0 to W//2 - 1).
4. If H >= W, the output grid is the top half of the input grid (rows 0 to H//2 - 1).
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by keeping either the left half or the top half,
    depending on whether the width or height is greater.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed output grid.
    """
    # Convert input_grid to a numpy array if it isn't already
    input_grid_np = np.array(input_grid)

    # 1. Determine the height (H) and width (W) of the input grid.
    H, W = input_grid_np.shape

    # 2. Compare the width (W) and height (H).
    if W > H:
        # 3. If the width (W) is greater than the height (H),
        #    keep the left half of the input grid.
        #    Calculate the midpoint width using integer division.
        mid_W = W // 2
        # Slice the array to keep columns 0 to mid_W - 1.
        output_grid = input_grid_np[:, :mid_W]
    else:
        # 4. Otherwise (if the height (H) is greater than or equal to the width (W)),
        #    keep the top half of the input grid.
        #    Calculate the midpoint height using integer division.
        mid_H = H // 2
        # Slice the array to keep rows 0 to mid_H - 1.
        output_grid = input_grid_np[:mid_H, :]

    return output_grid.tolist() # Convert back to list of lists if needed, or return np.array
