import numpy as np

"""
The transformation identifies a 2x2 block of non-white pixels within the input grid. 
It then copies the input grid to the output grid. 
Finally, it fills the four 2x2 corner areas of the output grid with colors derived 
from the pixels of the input 2x2 block, following a 180-degree rotational mapping:
- The input block's top-left pixel color fills the output's bottom-right corner.
- The input block's top-right pixel color fills the output's bottom-left corner.
- The input block's bottom-left pixel color fills the output's top-right corner.
- The input block's bottom-right pixel color fills the output's top-left corner.
"""

def find_2x2_block(grid):
    """
    Finds the top-left coordinate (row, col) of the first 2x2 block 
    containing only non-white (non-zero) pixels.
    
    Args:
        grid (np.array): The input grid.

    Returns:
        tuple (int, int) or None: The (row, col) of the top-left pixel 
                                   of the block, or None if not found.
    """
    rows, cols = grid.shape
    for r in range(rows - 1):
        for c in range(cols - 1):
            # Check if all four pixels in the 2x2 area are non-white
            if (grid[r, c] != 0 and 
                grid[r, c+1] != 0 and 
                grid[r+1, c] != 0 and 
                grid[r+1, c+1] != 0):
                return r, c
    return None # Should not happen based on task description

def transform(input_grid):
    """
    Applies the described transformation to the input grid.
    
    Args:
        input_grid (list of lists or np.array): The input grid.

    Returns:
        np.array: The transformed output grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_np)
    
    # Find the 2x2 non-white block in the input
    block_coords = find_2x2_block(input_np)
    
    if block_coords is None:
        # Handle case where block is not found, though unlikely for this task
        print("Warning: 2x2 non-white block not found.")
        return output_grid # Return unchanged grid or handle error appropriately

    r, c = block_coords
    
    # Extract the colors from the input block
    color_tl = input_np[r, c]
    color_tr = input_np[r, c+1]
    color_bl = input_np[r+1, c]
    color_br = input_np[r+1, c+1]
    
    # Fill the corners of the output grid based on the mapped colors
    # Top-left corner (0:2, 0:2) gets bottom-right color
    output_grid[0:2, 0:2] = color_br
    
    # Top-right corner (0:2, 4:6) gets bottom-left color
    output_grid[0:2, 4:6] = color_bl
    
    # Bottom-left corner (4:6, 0:2) gets top-right color
    output_grid[4:6, 0:2] = color_tr
    
    # Bottom-right corner (4:6, 4:6) gets top-left color
    output_grid[4:6, 4:6] = color_tl

    return output_grid