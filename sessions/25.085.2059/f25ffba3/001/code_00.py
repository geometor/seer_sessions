"""
Create an output grid by reflecting the bottom half of the input grid 
into the top half and copying the bottom half directly into the output's 
bottom half. The transformation effectively creates vertical symmetry 
around the horizontal midline of the grid, using the content from the 
input's bottom half.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by vertically reflecting its bottom half 
    into the top half of the output grid and copying the bottom half 
    directly to the output's bottom half.

    Args:
        input_grid (list of lists): A 2D list representing the input grid.

    Returns:
        list of lists: A 2D list representing the transformed output grid.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    
    # Get the dimensions of the grid
    height, width = input_array.shape
    
    # Calculate the middle row index (integer division handles even heights)
    mid_row = height // 2
    
    # Extract the bottom half of the input grid
    # Slicing includes the mid_row up to the end
    bottom_half = input_array[mid_row:, :]
    
    # Create a vertically flipped version of the bottom half
    # np.flipud flips an array vertically (up-down)
    flipped_bottom_half = np.flipud(bottom_half)
    
    # Initialize the output grid as a copy of the input initially,
    # or create an empty grid of the same size. Using an empty grid might be safer.
    output_array = np.zeros_like(input_array) 
    
    # Place the flipped bottom half into the top half of the output grid
    # Slicing goes from the start up to (but not including) the mid_row
    output_array[:mid_row, :] = flipped_bottom_half
    
    # Place the original bottom half into the bottom half of the output grid
    # Slicing includes the mid_row up to the end
    output_array[mid_row:, :] = bottom_half
    
    # Convert the numpy array back to a list of lists for the return value
    output_grid = output_array.tolist()
    
    return output_grid
