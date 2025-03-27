import numpy as np

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
4. Copying the original 2x2 block from the input grid (at location r, c) 
   to the *same* location (r, c) in the output grid. This step overwrites 
   any background pixels or potentially parts of the corner blocks if the 
   original block was located near or in a corner.
"""

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
                return (r, c), (A, B, C, D)
    return None, None # Should not happen based on task description

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

    # 1. Identify the source 2x2 block and its properties
    block_coords, block_colors = find_2x2_block(input_np)

    # Handle the unlikely case where no block is found
    if block_coords is None:
        print("Warning: No 2x2 non-white block found in input.")
        # Return a copy of the input or an empty grid of the same size
        return input_grid 

    r, c = block_coords
    A, B, C, D = block_colors
    
    # 2. Initialize the output grid with the background color (white, 0)
    output_grid = np.zeros_like(input_np)

    # 3. Fill the corner 2x2 blocks
    # Fill the top-left 2x2 corner with color D (bottom-right of input block)
    output_grid[0:2, 0:2] = D
    # Fill the top-right 2x2 corner with color C (bottom-left of input block)
    output_grid[0:2, 4:6] = C
    # Fill the bottom-left 2x2 corner with color B (top-right of input block)
    output_grid[4:6, 0:2] = B
    # Fill the bottom-right 2x2 corner with color A (top-left of input block)
    output_grid[4:6, 4:6] = A

    # 4. Copy the original 2x2 block to its original location in the output grid
    # Extract the original block from the input
    original_block = input_np[r:r+2, c:c+2]
    # Place it at its original position in the output, overwriting if necessary
    output_grid[r:r+2, c:c+2] = original_block

    # Convert the final numpy array back to a list of lists before returning
    return output_grid.tolist()