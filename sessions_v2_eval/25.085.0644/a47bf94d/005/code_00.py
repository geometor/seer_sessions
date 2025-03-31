"""
Identify all 3x3 subgrids within the input grid that consist entirely of a single, non-white color.
For each such identified 3x3 block of color C, replace it with a checkerboard pattern:
- The center pixel becomes white (0).
- The four corner pixels become white (0).
- The four edge pixels (top-center, bottom-center, left-center, right-center) retain the original color C.
All other pixels in the grid that are not part of such a transformed 3x3 block retain their original color.
"""

import numpy as np

def _is_solid_3x3(grid, r, c):
    """
    Checks if the 3x3 subgrid starting at (r, c) is solid non-white.

    Args:
        grid (np.array): The input grid.
        r (int): Top row index of the 3x3 subgrid.
        c (int): Left column index of the 3x3 subgrid.

    Returns:
        tuple (bool, int): (True, color) if the block is solid non-white,
                           (False, -1) otherwise. Returns -1 for color if not solid.
    """
    # Check dimensions: ensure we can extract a 3x3 grid
    height, width = grid.shape
    if r + 3 > height or c + 3 > width:
        return False, -1

    # Get the color of the top-left pixel
    color = grid[r, c]

    # Check if the color is white (0)
    if color == 0:
        return False, -1

    # Check if all 9 pixels in the 3x3 block have the same color
    for i in range(r, r + 3):
        for j in range(c, c + 3):
            if grid[i, j] != color:
                return False, -1

    # If all checks pass, it's a solid non-white block
    return True, color

def transform(input_grid):
    """
    Transforms the input grid by replacing solid 3x3 non-white blocks
    with a specific checkerboard pattern.

    Args:
        input_grid (list of lists or np.array): The input grid.

    Returns:
        list of lists: The transformed output grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)

    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_np)

    # Get grid dimensions
    height, width = input_np.shape

    # Iterate through all possible top-left corners (r, c) of a 3x3 block
    # r goes from 0 to height-3, c goes from 0 to width-3
    for r in range(height - 2):
        for c in range(width - 2):
            # Check if the 3x3 block starting at (r, c) is solid non-white
            is_solid, color = _is_solid_3x3(input_np, r, c)

            if is_solid:
                # Apply the checkerboard pattern to the output grid
                # Corners become white (0)
                output_grid[r, c] = 0
                output_grid[r, c + 2] = 0
                output_grid[r + 2, c] = 0
                output_grid[r + 2, c + 2] = 0
                # Center becomes white (0)
                output_grid[r + 1, c + 1] = 0
                # Edges keep the original color (already set by copy, but good to be explicit)
                # output_grid[r, c+1] = color
                # output_grid[r+1, c] = color
                # output_grid[r+1, c+2] = color
                # output_grid[r+2, c+1] = color
                # Note: We directly modify the output_grid based on the input_np check.
                # This avoids issues if blocks overlap, as the check always refers
                # to the original input state.

    # Return the modified output grid as a list of lists
    return output_grid.tolist()