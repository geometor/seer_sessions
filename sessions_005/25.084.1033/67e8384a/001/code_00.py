"""
Constructs an output grid that is twice the height and twice the width of the input grid.
The output grid is composed of four quadrants, each being a 3x3 subgrid derived from the input grid:
- Top-left quadrant: An identical copy of the input grid.
- Top-right quadrant: A horizontal reflection (flipped left-to-right) of the input grid.
- Bottom-left quadrant: A vertical reflection (flipped top-to-bottom) of the input grid.
- Bottom-right quadrant: Both a horizontal and vertical reflection (equivalent to a 180-degree rotation) of the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by creating a 2x2 arrangement of the input grid
    and its reflections.
    """
    # Convert the input list of lists to a numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)

    # Get the dimensions of the input grid
    height, width = input_array.shape

    # Create the four transformed quadrants
    # 1. Top-left: Original grid
    original = input_array

    # 2. Top-right: Horizontal flip (left-right)
    flipped_h = np.fliplr(input_array)

    # 3. Bottom-left: Vertical flip (up-down)
    flipped_v = np.flipud(input_array)

    # 4. Bottom-right: Horizontal and vertical flip (180-degree rotation)
    # Can be achieved by flipping horizontally then vertically, or vice-versa
    flipped_hv = np.fliplr(flipped_v) # or np.flipud(flipped_h)

    # Construct the output grid by combining the quadrants
    # Combine top-left and top-right horizontally
    top_row = np.hstack((original, flipped_h))

    # Combine bottom-left and bottom-right horizontally
    bottom_row = np.hstack((flipped_v, flipped_hv))

    # Combine the top row and bottom row vertically
    output_grid = np.vstack((top_row, bottom_row))

    # Return the result as a list of lists (standard ARC format)
    return output_grid.tolist()
