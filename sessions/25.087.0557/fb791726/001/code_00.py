"""
Duplicate the input grid into the top-left and bottom-right quadrants 
of a doubled-size output grid, inserting a green horizontal and vertical 
line through the middle.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by duplicating it diagonally in a doubled-size grid
    and inserting green dividing lines.

    Args:
        input_grid (list of lists): The input grid.

    Returns:
        numpy.ndarray: The transformed grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    
    # Determine dimensions H and W of input_grid.
    H, W = input_np.shape
    
    # Define output dimensions
    output_H = 2 * H
    output_W = 2 * W
    
    # Define colors
    background_color = 0
    green_color = 3
    
    # Create output_grid with dimensions (2*H) x (2*W), initialized with background_color.
    output_grid = np.full((output_H, output_W), background_color, dtype=int)
    
    # Copy input_grid to the top-left quadrant of output_grid.
    # Region from (row 0, col 0) to (row H-1, col W-1).
    output_grid[0:H, 0:W] = input_np
    
    # Copy input_grid to the bottom-right quadrant of output_grid.
    # Region from (row H, col W) to (row 2*H-1, col 2*W-1).
    output_grid[H:output_H, W:output_W] = input_np
    
    # Fill the middle horizontal row of output_grid with green_color.
    # Row index H, from column 0 to 2*W-1.
    output_grid[H, :] = green_color
    
    # Fill the middle vertical column of output_grid with green_color.
    # Column index W, from row 0 to 2*H-1.
    output_grid[:, W] = green_color
    
    return output_grid
