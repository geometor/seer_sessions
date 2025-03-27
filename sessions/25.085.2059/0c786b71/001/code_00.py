"""
Creates an output grid that is double the height and width of the input grid.
The output grid is composed of four quadrants, each the size of the input grid.
The top-left quadrant contains the input grid flipped horizontally and vertically.
The top-right quadrant contains the input grid flipped vertically.
The bottom-left quadrant contains the input grid flipped horizontally.
The bottom-right quadrant contains the original input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by creating a 2x2 arrangement of transformed
    versions of the input.

    Args:
        input_grid (list of lists): The input grid represented as a 2D list.

    Returns:
        list of lists: The transformed output grid.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)

    # Get the dimensions of the input grid
    H, W = input_array.shape

    # Create the output grid with double the dimensions, initialized with zeros
    output_grid = np.zeros((2 * H, 2 * W), dtype=int)

    # Generate the transformed versions of the input grid
    original = input_array
    h_flipped = np.fliplr(input_array) # Flip horizontally (left-right)
    v_flipped = np.flipud(input_array) # Flip vertically (up-down)
    hv_flipped = np.flipud(np.fliplr(input_array)) # Flip both horizontally and vertically

    # Place the transformed grids into the corresponding quadrants of the output grid
    # Top-Left Quadrant: Flipped horizontally and vertically
    output_grid[0:H, 0:W] = hv_flipped

    # Top-Right Quadrant: Flipped vertically
    output_grid[0:H, W:2*W] = v_flipped

    # Bottom-Left Quadrant: Flipped horizontally
    output_grid[H:2*H, 0:W] = h_flipped

    # Bottom-Right Quadrant: Original input
    output_grid[H:2*H, W:2*W] = original

    # Convert the numpy array back to a list of lists for the final output format
    return output_grid.tolist()
