"""
Replaces each blue (1) pixel in the input grid with a 3x3 block of pixels.
The 3x3 block is centered on the original blue pixel's location. The block's
colors are:
- Top row: Orange (7), Blue (1), Magenta (6)
- Middle row: Red (2), White (0), Azure (8)
- Bottom row: Rotates clockwise: starts as [2,0,8] then becomes [7,1,6], then repeats
All other pixels remain unchanged.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    
    # Find the locations of all blue (1) pixels
    blue_pixel_locations = np.argwhere(input_grid == 1)
    
    # Counter to track the rotation of the bottom row, starts at -1 so first instance is 0
    pattern_index = -1
    
    bottom_row_patterns = [[2, 0, 8], [7, 1, 6]]

    # Iterate through each blue pixel location
    for row, col in blue_pixel_locations:
        pattern_index = (pattern_index + 1) % 2
        
        # Define the 3x3 replacement block
        replacement_block = np.array([
            [7, 1, 6],
            [2, 0, 8],
            bottom_row_patterns[pattern_index]
        ])
        
        # Calculate the starting row and column for placing the 3x3 block
        start_row = row - 1
        start_col = col - 1
        
        # Replace the corresponding section of the output grid with the replacement block
        # Handle boundary conditions to prevent index out of bounds errors
        for i in range(3):
            for j in range(3):
                output_row = start_row + i
                output_col = start_col + j
                #check output grid bounds
                if 0 <= output_row < output_grid.shape[0] and 0 <= output_col < output_grid.shape[1]:
                    output_grid[output_row, output_col] = replacement_block[i, j]

    return output_grid