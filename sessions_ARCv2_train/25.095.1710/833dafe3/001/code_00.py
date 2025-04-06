"""
Construct a larger grid (2Nx2N) by arranging four transformed versions of the input grid (NxN).
The four quadrants are arranged as follows:
Top-Left (TL): Input rotated 180 degrees.
Top-Right (TR): Input flipped vertically.
Bottom-Left (BL): Input flipped horizontally.
Bottom-Right (BR): Original input.
"""

import numpy as np

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms an NxN input grid into a 2Nx2N output grid by arranging
    rotated and flipped versions of the input grid.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    n = input_np.shape[0] # Get the size N of the input grid

    # Calculate the four quadrants using numpy functions
    # TL: Rotate 180 degrees (equivalent to two 90-degree rotations)
    tl_quadrant = np.rot90(input_np, 2)

    # TR: Flip vertically (up-down)
    tr_quadrant = np.flipud(input_np)

    # BL: Flip horizontally (left-right)
    bl_quadrant = np.fliplr(input_np)

    # BR: Original input grid
    br_quadrant = input_np

    # Assemble the output grid using numpy block concatenation
    # Arrange the quadrants in a 2x2 layout
    output_np = np.block([
        [tl_quadrant, tr_quadrant],
        [bl_quadrant, br_quadrant]
    ])

    # Convert the resulting numpy array back to a list of lists
    output_grid = output_np.tolist()

    return output_grid