"""
Identify all solid 3x3 squares composed of a single non-white color within the input grid.
For each identified 3x3 square, change the color of its central pixel to white (0) in the output grid.
All other pixels retain their original color and position from the input grid.
"""

import numpy as np

def _is_solid_3x3(grid, r, c):
    """
    Checks if the 3x3 subgrid starting at (r, c) is solid and non-white.
    
    Args:
        grid (np.array): The input grid.
        r (int): Starting row index.
        c (int): Starting column index.
        
    Returns:
        bool: True if the 3x3 subgrid is solid and non-white, False otherwise.
    """
    # Get the color of the top-left pixel
    color = grid[r, c]
    
    # Check if the color is white (background)
    if color == 0:
        return False
        
    # Check if all 9 pixels in the 3x3 subgrid have the same color
    for i in range(r, r + 3):
        for j in range(c, c + 3):
            if grid[i, j] != color:
                return False
                
    return True

def transform(input_grid):
    """
    Transforms the input grid by hollowing out the center of solid 3x3 squares.
    
    Args:
        input_grid (list of lists or np.array): The input grid.
        
    Returns:
        np.array: The transformed output grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_np)
    
    # Get grid dimensions
    height, width = input_np.shape
    
    # Iterate through the grid to find potential top-left corners of 3x3 squares
    # The loops stop at height-2 and width-2 to ensure a full 3x3 subgrid exists
    for r in range(height - 2):
        for c in range(width - 2):
            # Check if the 3x3 subgrid starting at (r, c) is solid and non-white
            if _is_solid_3x3(input_np, r, c):
                # If it is, set the center pixel (r+1, c+1) in the output grid to white (0)
                output_grid[r + 1, c + 1] = 0
                
    # Return the modified output grid
    return output_grid.tolist() # Convert back to list of lists if required by ARC framework
