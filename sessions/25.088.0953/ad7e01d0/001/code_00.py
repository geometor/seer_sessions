"""
Transforms an input grid based on the following rule:
1. Determine the dimensions (H, W) of the input grid.
2. Create an output grid with dimensions (H*H, W*W).
3. Iterate through each pixel (r, c) of the input grid.
4. If the pixel at input_grid[r, c] is gray (5):
    - Place a copy of the original input grid into the corresponding HxW tile in the output grid, starting at output_grid[r*H, c*W].
5. If the pixel at input_grid[r, c] is not gray (5):
    - Place an HxW tile filled entirely with white (0) into the corresponding HxW tile in the output grid, starting at output_grid[r*H, c*W].
"""

import numpy as np

def transform(input_grid):
    """
    Applies the conditional tiling transformation to the input grid.

    Args:
        input_grid (list of lists or numpy array): The input grid.

    Returns:
        numpy array: The transformed output grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    H, W = input_np.shape

    # Define constants
    trigger_color = 5  # gray
    background_color = 0 # white

    # Calculate output dimensions
    output_H = H * H
    output_W = W * W

    # Initialize the output grid with the background color
    output_grid = np.full((output_H, output_W), background_color, dtype=int)

    # Create a template white tile
    white_tile = np.full((H, W), background_color, dtype=int)

    # Iterate through each pixel of the input grid
    for r in range(H):
        for c in range(W):
            # Determine the top-left corner of the target tile in the output grid
            start_row = r * H
            start_col = c * W
            
            # Check the color of the current input pixel
            if input_np[r, c] == trigger_color:
                # If the color is gray, copy the original input grid to the tile
                output_grid[start_row : start_row + H, start_col : start_col + W] = input_np
            else:
                # If the color is not gray, copy the white tile
                output_grid[start_row : start_row + H, start_col : start_col + W] = white_tile

    return output_grid.tolist() # Convert back to list of lists if needed by the environment
