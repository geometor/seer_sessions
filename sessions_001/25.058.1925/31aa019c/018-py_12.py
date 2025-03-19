"""
Create an output grid. The output grid size seems independent to the input grid. The examples tested seem to adhere to two sizes, 10x10 and 5x5. Create a 3x3 square block of red (2) pixels. Place the 3x3 block in the top-right corner of the *output* grid. Change the color of the center pixel of the 3x3 block to magenta (6).
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid, choosing between 10x10 and 5x5.
    # For now, prioritize 10x10, but this might need a more sophisticated selection mechanism.
    output_size = 10 if len(input_grid) % 2 == 0 else 5
    output_grid = np.zeros((output_size, output_size), dtype=int)
    
    # Define the dimensions of the block
    block_size = 3

    # Determine the starting row and column for the block (top-right corner)
    start_row = 0
    start_col = output_grid.shape[1] - block_size
    
    #Check if the placement is within bounds. This only occurs on a 5 x 5.
    if start_row >= 0 and start_col >= 0:
       # Fill the 3x3 block with red (2)
       output_grid[start_row:start_row + block_size, start_col:start_col + block_size] = 2

       # Change the center pixel of the block to magenta (6)
       center_row = start_row + block_size // 2
       center_col = start_col + block_size // 2
       output_grid[center_row, center_col] = 6

    return output_grid