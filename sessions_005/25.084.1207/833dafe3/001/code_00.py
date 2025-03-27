"""
Constructs a larger grid by tiling four reflected versions of the input grid.
The output grid has dimensions double those of the input grid (2*H x 2*W).
The four quadrants of the output grid are filled as follows:
- Top-Left: Input grid flipped horizontally and vertically.
- Top-Right: Input grid flipped vertically.
- Bottom-Left: Input grid flipped horizontally.
- Bottom-Right: Original input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Applies the tiling and reflection transformation to the input grid.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A numpy array representing the transformed output grid.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    H, W = input_array.shape

    # Create the flipped versions of the input grid
    # Horizontal flip (left-right)
    h_flipped = np.fliplr(input_array)
    # Vertical flip (top-bottom)
    v_flipped = np.flipud(input_array)
    # Horizontal and vertical flip (equivalent to 180-degree rotation)
    hv_flipped = np.flipud(h_flipped) # Or np.fliplr(v_flipped)

    # Initialize the output grid with dimensions 2*H x 2*W
    # Use the same dtype as the input to preserve color values
    output_grid = np.zeros((2 * H, 2 * W), dtype=input_array.dtype)

    # Populate the four quadrants of the output grid
    # Top-Left quadrant: HV flipped version
    output_grid[0:H, 0:W] = hv_flipped

    # Top-Right quadrant: Vertically flipped version
    output_grid[0:H, W:2*W] = v_flipped

    # Bottom-Left quadrant: Horizontally flipped version
    output_grid[H:2*H, 0:W] = h_flipped

    # Bottom-Right quadrant: Original input grid
    output_grid[H:2*H, W:2*W] = input_array

    return output_grid.tolist() # Convert back to list of lists if required by spec, although numpy is often fine