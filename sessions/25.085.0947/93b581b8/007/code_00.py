"""
Transforms a 6x6 input grid containing one 2x2 block of non-white pixels.
The transformation involves:
1. Identifying the single 2x2 block of non-white pixels in the input grid.
   Let its top-left coordinate be (r, c) and its pixels be A (top-left),
   B (top-right), C (bottom-left), D (bottom-right).
2. Creating a new 6x6 output grid, initialized with the background color (white, 0).
3. Filling four 2x2 blocks in the corners of the output grid with colors
   derived from the input block's pixels:
   - Top-left corner (rows 0-1, cols 0-1) gets color D.
   - Top-right corner (rows 0-1, cols 4-5) gets color C.
   - Bottom-left corner (rows 4-5, cols 0-1) gets color B.
   - Bottom-right corner (rows 4-5, cols 4-5) gets color A.
The original 2x2 block from the input is *not* copied to the output.
"""

import numpy as np

def find_2x2_block(grid):
    """
    Finds the top-left corner coordinates (r, c) and the four pixel values
    (A, B, C, D) of the first 2x2 block containing only non-zero (non-white) values.

    Args:
        grid (np.array): The input grid.

    Returns:
        tuple: A tuple containing:
            - tuple: The (row, column) of the top-left pixel of the block.
            - tuple: The colors (A, B, C, D) of the block's pixels in the order:
                     top-left, top-right, bottom-left, bottom-right.
        Returns (None, None) if no such block is found.
    """
    height, width = grid.shape
    for r in range(height - 1):
        for c in range(width - 1):
            # Extract the 2x2 subgrid
            subgrid = grid[r:r+2, c:c+2]
            # Check if all elements are non-zero (non-white)
            if np.all(subgrid != 0):
                A = subgrid[0, 0] # Top-left
                B = subgrid[0, 1] # Top-right
                C = subgrid[1, 0] # Bottom-left
                D = subgrid[1, 1] # Bottom-right
                # Return the location (r, c) and the colors (A, B, C, D)
                return (r, c), (A, B, C, D)
    return None, None # Should not happen based on task description if input is valid

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed output grid.
    """
    # Convert input list to a numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape # Should be 6x6 based on examples

    # 1. Identify the source 2x2 block and its properties
    block_coords, block_colors = find_2x2_block(input_np)

    # Handle the unlikely case where no block is found
    if block_coords is None:
        print("Warning: No 2x2 non-white block found in input.")
        # Return an empty grid of the same size as a fallback
        return np.zeros_like(input_np).tolist()

    # Extract the four colors A, B, C, D from the found block
    A, B, C, D = block_colors

    # 2. Initialize the output grid with the background color (white, 0)
    output_grid = np.zeros_like(input_np)

    # 3. Fill the corner 2x2 blocks based on the identified colors
    # Fill the top-left 2x2 corner (0:2, 0:2) with color D (bottom-right of input block)
    output_grid[0:2, 0:2] = D
    # Fill the top-right 2x2 corner (0:2, 4:6) with color C (bottom-left of input block)
    # Note: Python slicing excludes the end index, so width-2:width means cols 4 and 5
    output_grid[0:2, width-2:width] = C
    # Fill the bottom-left 2x2 corner (4:6, 0:2) with color B (top-right of input block)
    # Note: height-2:height means rows 4 and 5
    output_grid[height-2:height, 0:2] = B
    # Fill the bottom-right 2x2 corner (4:6, 4:6) with color A (top-left of input block)
    output_grid[height-2:height, width-2:width] = A

    # 4. The original block is NOT copied. The grid with only the corners filled is the result.

    # Convert the final numpy array back to a list of lists before returning
    return output_grid.tolist()