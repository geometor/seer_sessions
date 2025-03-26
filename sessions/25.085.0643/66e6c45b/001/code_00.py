import numpy as np

"""
Transforms an input grid by finding a 2x2 block of non-white pixels and relocating those four pixels to the corners of an otherwise white output grid of the same dimensions.

1.  Initialize an output grid with the same dimensions as the input grid, filling it entirely with the white color (0).
2.  Scan the input grid to locate a 2x2 block where all four pixels have non-white colors. Record the colors and their positions within this block (top-left, top-right, bottom-left, bottom-right). Let the top-left coordinate of this block in the input be (r, c).
3.  Place the color found at the input block's top-left position (r, c) into the output grid's top-left corner (0, 0).
4.  Place the color found at the input block's top-right position (r, c+1) into the output grid's top-right corner (0, width-1), where width is the width of the grid.
5.  Place the color found at the input block's bottom-left position (r+1, c) into the output grid's bottom-left corner (height-1, 0), where height is the height of the grid.
6.  Place the color found at the input block's bottom-right position (r+1, c+1) into the output grid's bottom-right corner (height-1, width-1).
7.  The resulting grid is the final output.
"""

def find_2x2_block(grid):
    """
    Finds the top-left coordinate (r, c) of the first 2x2 block 
    where all four pixels are non-white (non-zero).

    Args:
        grid (np.array): The input grid.

    Returns:
        tuple (int, int) or None: The (row, col) of the top-left corner 
                                    of the block, or None if not found.
    """
    height, width = grid.shape
    for r in range(height - 1):
        for c in range(width - 1):
            # Check if all four pixels in the 2x2 block starting at (r, c) are non-zero
            if (grid[r, c] != 0 and
                grid[r, c+1] != 0 and
                grid[r+1, c] != 0 and
                grid[r+1, c+1] != 0):
                return r, c
    return None # No such block found

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # Convert input list of lists to numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    height, width = input_array.shape
    
    # 1. Initialize an output grid with the same dimensions as the input grid, 
    #    filling it entirely with the white color (0).
    output_grid = np.zeros((height, width), dtype=int)

    # 2. Scan the input grid to locate the 2x2 block of non-white pixels.
    block_coord = find_2x2_block(input_array)

    # Proceed only if a block was found
    if block_coord:
        r, c = block_coord
        
        # Extract the colors from the identified block
        top_left_color = input_array[r, c]
        top_right_color = input_array[r, c+1]
        bottom_left_color = input_array[r+1, c]
        bottom_right_color = input_array[r+1, c+1]

        # 3. Place the color from input (r, c) -> output top-left corner (0, 0).
        output_grid[0, 0] = top_left_color
        
        # 4. Place the color from input (r, c+1) -> output top-right corner (0, width-1).
        output_grid[0, width-1] = top_right_color
        
        # 5. Place the color from input (r+1, c) -> output bottom-left corner (height-1, 0).
        output_grid[height-1, 0] = bottom_left_color
        
        # 6. Place the color from input (r+1, c+1) -> output bottom-right corner (height-1, width-1).
        output_grid[height-1, width-1] = bottom_right_color
        
    # 7. The resulting grid is the final output. 
    # If no block was found, the all-white grid initialized earlier is returned.
    return output_grid.tolist() # Convert back to list of lists if required by the environment