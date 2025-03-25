"""
Expands contiguous blocks of non-white pixels to the left until a non-white pixel of a different color or the grid edge is encountered.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by expanding contiguous blocks of non-white pixels to the left.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed grid.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each row
    for r in range(rows):
        # Iterate through each pixel in the row, from right to left, to identify blocks
        c = 0
        while c < cols:
            # Check if the pixel is non-white
            if input_grid[r, c] != 0:
                # Find the end of the contiguous block
                block_end = c
                while block_end + 1 < cols and input_grid[r, block_end + 1] == input_grid[r, c]:
                    block_end += 1

                # Expand the block to the left
                for c_left in range(c - 1, -1, -1):
                    if output_grid[r, c_left] == 0:  # Check for white
                        output_grid[r, c_left] = input_grid[r, c]
                    else:
                        break # Stop if hit non-white or edge

                # Move c past this block
                c = block_end + 1
            else:
                c += 1

    return output_grid