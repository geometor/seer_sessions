"""
The transformation takes an input grid and produces an output grid with the same height but double the width. 
The left half of the output grid is identical to the input grid.
The right half of the output grid is a horizontal reflection (mirror image) of the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by concatenating it with its horizontal reflection.

    Args:
        input_grid (list of lists): A 2D list representing the input grid.

    Returns:
        list of lists: A 2D list representing the transformed output grid.
    """
    # Convert the input list of lists to a NumPy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    
    # Get the height (H) and width (W) of the input grid
    H, W = input_np.shape
    
    # Calculate the width of the output grid
    output_width = 2 * W
    
    # Create the output grid initialized with zeros (or any default value)
    # Using the same dtype as the input is generally a good practice
    output_np = np.zeros((H, output_width), dtype=input_np.dtype) 
    
    # Copy the original input grid to the left half of the output grid
    # output_np[:, 0:W] covers all rows and columns from 0 up to (but not including) W
    output_np[:, :W] = input_np
    
    # Create a horizontally flipped version of the input grid
    flipped_input_np = np.fliplr(input_np)
    
    # Copy the flipped input grid to the right half of the output grid
    # output_np[:, W:output_width] covers all rows and columns from W up to (but not including) output_width
    output_np[:, W:] = flipped_input_np
    
    # Convert the resulting NumPy array back to a list of lists format
    output_grid = output_np.tolist()
    
    return output_grid
