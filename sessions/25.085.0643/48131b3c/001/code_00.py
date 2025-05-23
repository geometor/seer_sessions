"""
Create an output grid by tiling the input grid in a 2x2 arrangement.
The output grid's dimensions will be double the input grid's dimensions (height 2*H, width 2*W).
The input grid is copied identically into the top-left, top-right, bottom-left, and bottom-right quadrants of the output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Tiles the input grid in a 2x2 pattern to create the output grid.

    Args:
        input_grid (list of lists or np.ndarray): The input grid.

    Returns:
        np.ndarray: The transformed output grid.
    """
    # Convert input grid to a numpy array for easier slicing
    input_np = np.array(input_grid, dtype=int)
    
    # Determine the height (H) and width (W) of the input grid
    H, W = input_np.shape
    
    # Calculate the dimensions of the output grid
    output_H = 2 * H
    output_W = 2 * W
    
    # Create a new output grid filled with zeros (or any default value)
    output_grid = np.zeros((output_H, output_W), dtype=int)
    
    # Copy the input grid to the top-left quadrant
    # Rows 0 to H-1, Columns 0 to W-1
    output_grid[0:H, 0:W] = input_np
    
    # Copy the input grid to the top-right quadrant
    # Rows 0 to H-1, Columns W to 2*W-1
    output_grid[0:H, W:output_W] = input_np
    
    # Copy the input grid to the bottom-left quadrant
    # Rows H to 2*H-1, Columns 0 to W-1
    output_grid[H:output_H, 0:W] = input_np
    
    # Copy the input grid to the bottom-right quadrant
    # Rows H to 2*H-1, Columns W to 2*W-1
    output_grid[H:output_H, W:output_W] = input_np
    
    # Return the resulting output grid
    return output_grid.tolist() # Return as list of lists if required by ARC standard
