"""
Rearrange scattered colored pixels from an input grid into a 3x3 output grid.
The input grid is conceptually divided into a 3x3 grid of equal-sized rectangular blocks. 
Each block in the input's 3x3 division contains exactly one non-white pixel.
The color of the non-white pixel found within the block at position (Block Row, Block Col) 
in the input's 3x3 division is placed at position (Row, Col) in the 3x3 output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by finding the non-white pixel in each 3x3 block 
    and placing it into the corresponding cell of a 3x3 output grid.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 3x3 numpy array representing the transformed output grid.
    """
    # Convert input_grid to numpy array if it's not already
    input_grid_np = np.array(input_grid)
    
    # Get input grid dimensions
    H, W = input_grid_np.shape
    
    # Calculate the dimensions of the subgrids (blocks)
    # Assuming H and W are divisible by 3 based on the examples and analysis
    block_height = H // 3
    block_width = W // 3
    
    # Initialize a 3x3 output grid with white (0) pixels
    output_grid = np.zeros((3, 3), dtype=int)
    
    # Iterate through the 3x3 grid of blocks in the input
    for br in range(3):  # block row index
        for bc in range(3):  # block column index
            
            # Define the boundaries of the current block
            start_row = br * block_height
            end_row = start_row + block_height
            start_col = bc * block_width
            end_col = start_col + block_width
            
            # Scan the pixels within this block to find the non-white pixel
            found = False
            for r in range(start_row, end_row):
                for c in range(start_col, end_col):
                    pixel_color = input_grid_np[r, c]
                    if pixel_color != 0:  # Found a non-white pixel
                        # Place its color into the output grid at coordinates (br, bc)
                        output_grid[br, bc] = pixel_color
                        found = True
                        break # Exit inner column loop once pixel is found
                if found:
                    break # Exit outer row loop once pixel is found
                    
    return output_grid.tolist() # Return as list of lists, matching ARC format
