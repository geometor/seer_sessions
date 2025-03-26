"""
Construct a larger grid by tiling transformed versions of the input grid.
The output grid is twice the height and twice the width of the input grid.
The top-left quadrant is the original input grid.
The top-right quadrant is the input grid flipped horizontally.
The bottom-left quadrant is the input grid flipped vertically.
The bottom-right quadrant is the input grid flipped both horizontally and vertically.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by creating a 2x2 tiled arrangement of the
    original and flipped versions of the input grid.

    Args:
        input_grid (list[list[int]]): The input grid.

    Returns:
        list[list[int]]: The transformed output grid.
    """
    # Convert input list of lists to a NumPy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)

    # Determine the height (H) and width (W) of the input grid
    H, W = input_array.shape

    # Create a new output grid with height 2*H and width 2*W, initialized with zeros
    output_array = np.zeros((2 * H, 2 * W), dtype=int)

    # 1. Top-Left Quadrant: Copy the original input grid
    output_array[0:H, 0:W] = input_array

    # 2. Top-Right Quadrant: Create a horizontally flipped version and copy
    flipped_horizontal = np.fliplr(input_array)
    output_array[0:H, W:2*W] = flipped_horizontal

    # 3. Bottom-Left Quadrant: Create a vertically flipped version and copy
    flipped_vertical = np.flipud(input_array)
    output_array[H:2*H, 0:W] = flipped_vertical

    # 4. Bottom-Right Quadrant: Create a version flipped both horizontally and vertically and copy
    #    This can be done by flipping the vertically flipped version horizontally,
    #    or flipping the horizontally flipped version vertically.
    flipped_both = np.fliplr(flipped_vertical) # Or np.flipud(flipped_horizontal)
    output_array[H:2*H, W:2*W] = flipped_both

    # Convert the final NumPy array back to a list of lists
    output_grid = output_array.tolist()

    return output_grid
