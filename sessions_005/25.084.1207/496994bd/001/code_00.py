import numpy as np

"""
Identifies a block of non-white rows at the top of the input grid, 
creates a vertically flipped copy of this block, and places this flipped 
copy at the bottom of the grid, preserving the original top block and 
the white rows in between.
"""

def find_top_block_height(grid):
    """
    Finds the height of the contiguous block of non-white rows starting from the top.
    A row is considered non-white if it contains at least one non-white pixel.
    """
    height, width = grid.shape
    block_height = 0
    for r in range(height):
        # Check if all pixels in the row are white (0)
        if np.all(grid[r] == 0):
            break
        block_height += 1
    return block_height

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # Convert input list of lists to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_np)

    # 1. Identify the block of contiguous rows starting from the top (row 0)
    #    that contain at least one non-white pixel. Let its height be N.
    n = find_top_block_height(input_np)

    # If no non-white block is found at the top (n=0), return the original grid
    if n == 0:
        return output_grid.tolist()

    # 2. Extract the identified top block of N rows (from row 0 to row N-1).
    top_block = input_np[0:n, :]

    # 3. Create a vertically flipped version of this extracted block.
    flipped_block = np.flipud(top_block) # flipud reverses row order

    # 4. Place this flipped block into the output grid, starting at row H-N
    #    and ending at row H-1 (the bottom N rows).
    output_grid[height-n : height, :] = flipped_block

    # Return the modified output grid as a list of lists
    return output_grid.tolist()
