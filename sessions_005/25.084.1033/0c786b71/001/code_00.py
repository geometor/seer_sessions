"""
Construct a larger grid by arranging transformed versions of the input grid.
The output grid is twice the height and twice the width of the input grid.
It is composed of four quadrants, each the size of the input grid.
- The top-left quadrant contains the input grid rotated 180 degrees.
- The top-right quadrant contains the input grid flipped vertically.
- The bottom-left quadrant contains the input grid flipped horizontally.
- The bottom-right quadrant contains the original input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by creating a 2x2 arrangement of flipped/rotated versions.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    
    # Determine the height (H) and width (W) of the input grid
    H, W = input_np.shape

    # Create the transformed versions of the input grid
    # Flipped horizontally (left-right)
    flipped_h = np.fliplr(input_np)
    # Flipped vertically (up-down)
    flipped_v = np.flipud(input_np)
    # Rotated 180 degrees (equivalent to flipping both horizontally and vertically)
    rotated_180 = np.rot90(input_np, k=2) 
    # Alternatively: rotated_180 = np.flipud(np.fliplr(input_np))

    # Initialize the output grid with dimensions 2*H x 2*W
    output_grid = np.zeros((2 * H, 2 * W), dtype=int)

    # Populate the four quadrants of the output grid
    # Top-left quadrant (rows 0 to H-1, cols 0 to W-1)
    output_grid[0:H, 0:W] = rotated_180
    
    # Top-right quadrant (rows 0 to H-1, cols W to 2*W-1)
    output_grid[0:H, W:2*W] = flipped_v
    
    # Bottom-left quadrant (rows H to 2*H-1, cols 0 to W-1)
    output_grid[H:2*H, 0:W] = flipped_h
    
    # Bottom-right quadrant (rows H to 2*H-1, cols W to 2*W-1)
    output_grid[H:2*H, W:2*W] = input_np

    # Convert the numpy array back to a list of lists for the required output format
    return output_grid.tolist()
