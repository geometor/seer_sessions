"""
Identify the top 4x4 grid (G1, rows 0-3) and the bottom 4x4 grid (G2, rows 5-8) 
in the input grid, ignoring the separator row (row 4).
Create a new 4x4 output grid, initially filled with white (0).
Iterate through each cell position (row r, column c) from (0, 0) to (3, 3).
At each position (r, c), examine the color of the cell in G1 (color1) and the 
color of the corresponding cell in G2 (color2).
If exactly one of the cells is non-white (value is not 0) and the other is 
white (value is 0), set the corresponding cell (r, c) in the output grid to green (3).
Otherwise (if both are white or both are non-white), leave the corresponding 
cell (r, c) in the output grid as white (0).
Return the completed 4x4 output grid. This logic is equivalent to a bitwise 
XOR operation on the non-whiteness of the corresponding pixels.
"""

import numpy as np

def transform(input_grid):
    """
    Applies a cell-wise XOR logic based on non-whiteness between the top 
    and bottom 4x4 subgrids of the input.
    """
    
    # Extract the top 4x4 grid (G1)
    grid1 = input_grid[0:4, 0:4]
    
    # Extract the bottom 4x4 grid (G2) - note the row offset of 5
    grid2 = input_grid[5:9, 0:4]
    
    # Get the dimensions for iteration (assuming 4x4)
    height, width = grid1.shape
    
    # Initialize the output grid with white (0)
    output_grid = np.zeros((height, width), dtype=int)
    
    # Iterate through each cell position
    for r in range(height):
        for c in range(width):
            # Get the pixel values from the corresponding positions in G1 and G2
            pixel1 = grid1[r, c]
            pixel2 = grid2[r, c]
            
            # Determine if each pixel is non-white (not 0)
            is_pixel1_non_white = (pixel1 != 0)
            is_pixel2_non_white = (pixel2 != 0)
            
            # Apply XOR logic: if exactly one is non-white, set output to green (3)
            if is_pixel1_non_white ^ is_pixel2_non_white:
                output_grid[r, c] = 3
            # Otherwise, it remains white (0) by default initialization

    return output_grid
