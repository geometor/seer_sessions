"""
Identifies a central horizontal block of gray (5) pixels.
For each colored pixel (green 3, red 2, blue 1) found outside this block:
- If the pixel is above the block, it casts a gray (5) imprint onto the cell directly above the block in the same column.
- If the pixel is below the block, it casts a gray (5) imprint onto the cell directly below the block in the same column.
- If the original pixel was red (2) or blue (1), it is removed (changed to white 0) in the output. Green (3) pixels remain.
"""

import numpy as np

def find_gray_block_boundaries(grid):
    """
    Finds the top-most and bottom-most row indices of the gray (5) block.

    Args:
        grid (np.array): The input grid.

    Returns:
        tuple: (min_row, max_row) or (None, None) if no gray block is found.
    """
    gray_rows = np.where(grid == 5)[0]
    if len(gray_rows) == 0:
        return None, None
    return np.min(gray_rows), np.max(gray_rows)

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list): A list of lists representing the input grid.

    Returns:
        list: A list of lists representing the transformed output grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    output_np = np.copy(input_np)
    height, width = input_np.shape

    # Find the boundaries of the gray block
    min_gray_row, max_gray_row = find_gray_block_boundaries(input_np)

    # If no gray block exists, return the original grid (or handle as needed)
    # Based on examples, we assume a gray block always exists.
    if min_gray_row is None:
        return input_grid # Or raise an error, depending on requirements

    # Iterate through each cell of the input grid
    for r in range(height):
        for c in range(width):
            color = input_np[r, c]

            # Check if the pixel is one of the source colors (1, 2, 3)
            if color in [1, 2, 3]:
                # Check if the pixel is above the gray block
                if r < min_gray_row:
                    # Calculate the target row for the imprint (just above the block)
                    target_r = min_gray_row - 1
                    # Ensure the target row is within grid bounds
                    if 0 <= target_r < height:
                        # Place the gray imprint in the output grid
                        output_np[target_r, c] = 5
                # Check if the pixel is below the gray block
                elif r > max_gray_row:
                    # Calculate the target row for the imprint (just below the block)
                    target_r = max_gray_row + 1
                    # Ensure the target row is within grid bounds
                    if 0 <= target_r < height:
                        # Place the gray imprint in the output grid
                        output_np[target_r, c] = 5

                # Check if the original source pixel should be removed (colors 1 or 2)
                if color in [1, 2]:
                    # Change the original pixel location to white in the output grid
                    output_np[r, c] = 0
            # Note: If color == 3, the pixel at output_np[r, c] remains 3 because
            # output_np was initialized as a copy of input_np.

    # Convert the result back to a list of lists
    output_grid = output_np.tolist()
    return output_grid