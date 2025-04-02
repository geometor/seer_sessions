"""
The transformation identifies isolated non-white pixels in a 1D input grid. 
An isolated pixel is defined as a non-white pixel (color C) that has white pixels (color 0) or grid boundaries on both its immediate left and right. 
For each such isolated pixel, the transformation changes its adjacent white neighbors (left and right) to color C. 
Pixels that are part of a larger segment of non-white pixels, or white pixels not adjacent to an isolated non-white pixel, remain unchanged.
"""

import numpy as np

def find_foreground_color(grid):
    """Finds the single non-white color in the grid."""
    unique_colors = np.unique(grid)
    for color in unique_colors:
        if color != 0:
            return color
    return None # Should not happen based on examples, but good practice

def transform(input_grid):
    """
    Transforms the input grid by expanding isolated non-white pixels 
    into segments of three.
    """
    # Convert input list to numpy array for easier indexing
    input_np = np.array(input_grid, dtype=np.int8)
    
    # Handle cases where input might not be 2D list-of-lists initially
    if input_np.ndim == 1:
        input_np = input_np.reshape(1, -1)

    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_np)
    
    # Get grid dimensions (although height is always 1 here)
    height, width = input_np.shape
    
    # Find the non-white color used in this grid
    foreground_color = find_foreground_color(input_np)
    if foreground_color is None:
        # If grid is all white, return a copy
        return output_grid.tolist() 

    # Iterate through each pixel in the single row
    for i in range(width):
        # Check if the current pixel has the foreground color
        if input_np[0, i] == foreground_color:
            # Check conditions for expanding to the left
            # Condition: Left neighbor exists AND is white AND (Right neighbor doesn't exist OR is white)
            is_left_neighbor_white = (i > 0) and (input_np[0, i-1] == 0)
            is_right_side_clear = (i == width - 1) or (input_np[0, i+1] == 0)
            if is_left_neighbor_white and is_right_side_clear:
                output_grid[0, i-1] = foreground_color

            # Check conditions for expanding to the right
            # Condition: Right neighbor exists AND is white AND (Left neighbor doesn't exist OR is white)
            is_right_neighbor_white = (i < width - 1) and (input_np[0, i+1] == 0)
            is_left_side_clear = (i == 0) or (input_np[0, i-1] == 0)
            if is_right_neighbor_white and is_left_side_clear:
                output_grid[0, i+1] = foreground_color

    # Return the modified grid as a standard Python list of lists
    # For 1D input, return a list (as per example format)
    if height == 1:
         return output_grid.flatten().tolist()
    else: # General case if input were 2D
         return output_grid.tolist()
