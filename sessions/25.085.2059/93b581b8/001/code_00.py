import numpy as np

"""
Transformation Rule Natural Language Description:
1.  Start with the input 6x6 grid. Create a new 6x6 grid for the output, initially identical to the input grid.
2.  Locate the unique 2x2 block of non-white pixels within the input grid. Record the row and column `(r, c)` of its top-left pixel.
3.  Identify the colors of the four pixels of this input block:
    *   `color_TL` = color at `(r, c)`
    *   `color_TR` = color at `(r, c+1)`
    *   `color_BL` = color at `(r+1, c)`
    *   `color_BR` = color at `(r+1, c+1)`
4.  Modify the output grid by filling the four 2x2 corner areas according to the following rules:
    *   Fill the top-left 2x2 area (rows 0-1, columns 0-1) entirely with `color_BR`.
    *   Fill the top-right 2x2 area (rows 0-1, columns 4-5) entirely with `color_BL`.
    *   Fill the bottom-left 2x2 area (rows 3-4, columns 0-1) entirely with `color_TR`.
    *   Fill the bottom-right 2x2 area (rows 3-4, columns 4-5) entirely with `color_TL`.
5.  The resulting grid is the final output.
Note: This assumes a 6x6 grid and specific corner locations based on observations from training examples 2 and 3. Training example 1's output seems inconsistent with the pattern of filling the entire 2x2 corner block, but the consistent pattern is implemented here.
"""

def find_central_block_origin(grid: np.ndarray) -> tuple[int, int] | None:
    """
    Finds the top-left coordinate (r, c) of the first occurrence 
    of a 2x2 block where all pixels are non-white (non-zero).
    Assumes there is exactly one such block in a predominantly white grid.

    Args:
        grid: A numpy array representing the input grid.

    Returns:
        A tuple (row, column) of the top-left corner of the block, 
        or None if no such block is found.
    """
    H, W = grid.shape
    # Iterate through possible top-left corners of a 2x2 block
    for r in range(H - 1):
        for c in range(W - 1):
            # Check if all four pixels in the 2x2 block starting at (r, c) are non-white
            if (grid[r, c] != 0 and
                grid[r, c + 1] != 0 and
                grid[r + 1, c] != 0 and
                grid[r + 1, c + 1] != 0):
                # Found the block
                return r, c
    # Return None if no non-white 2x2 block is found (shouldn't happen based on task constraints)
    return None 

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by copying a central 2x2 block and creating 
    four new 2x2 blocks in the corners, colored based on the diagonally 
    opposite pixels of the central block.

    Args:
        input_grid: A list of lists representing the input grid (assumed 6x6).

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Convert input list of lists to a numpy array for efficient processing
    input_np = np.array(input_grid, dtype=int)
    
    # Check if grid is 6x6 as expected by the corner logic derived from examples
    H, W = input_np.shape
    if H != 6 or W != 6:
        # This implementation currently assumes a 6x6 grid for corner placement.
        # If grids of other sizes are possible, the corner logic would need generalization.
        print(f"Warning: Grid dimensions ({H}x{W}) are not 6x6. Corner logic might be incorrect.")
        # Attempt to proceed, but results might be wrong for non-6x6 grids.

    # Initialize the output grid as a copy of the input grid
    output_grid = np.copy(input_np)

    # Find the top-left corner (r, c) of the central 2x2 non-white block
    block_origin = find_central_block_origin(input_np)

    # If no block is found, return the original grid (or handle as error)
    if block_origin is None:
        print("Error: No 2x2 non-white block found.")
        return output_grid.tolist() 

    r, c = block_origin

    # Get the colors from the four pixels of the central block in the input
    color_TL = input_np[r, c]         # Top-Left pixel color
    color_TR = input_np[r, c + 1]     # Top-Right pixel color
    color_BL = input_np[r + 1, c]     # Bottom-Left pixel color
    color_BR = input_np[r + 1, c + 1] # Bottom-Right pixel color

    # --- Fill the corner 2x2 blocks in the output grid ---
    # Corner coordinates are hardcoded for a 6x6 grid based on examples.
    
    # Top-left corner (rows 0-1, cols 0-1) gets the color of the input block's Bottom-Right pixel (color_BR)
    output_grid[0:2, 0:2] = color_BR

    # Top-right corner (rows 0-1, cols 4-5) gets the color of the input block's Bottom-Left pixel (color_BL)
    output_grid[0:2, 4:6] = color_BL

    # Bottom-left corner (rows 3-4, cols 0-1) gets the color of the input block's Top-Right pixel (color_TR)
    output_grid[3:5, 0:2] = color_TR

    # Bottom-right corner (rows 3-4, cols 4-5) gets the color of the input block's Top-Left pixel (color_TL)
    output_grid[3:5, 4:6] = color_TL

    # Convert the final numpy array back to a list of lists for the expected output format
    return output_grid.tolist()