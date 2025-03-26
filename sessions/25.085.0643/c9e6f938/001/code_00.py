"""
This module defines a function to transform an input grid by concatenating it 
with its horizontal reflection. The output grid will have the same height as 
the input grid but double the width. The left half of the output grid is an 
exact copy of the input, and the right half is the input grid mirrored 
horizontally.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms an input grid by concatenating it with its horizontal reflection.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed grid.
    """
    # Convert the input list of lists to a NumPy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    
    # Get the dimensions of the input grid
    height, width = input_np.shape
    
    # Calculate the width of the output grid
    output_width = 2 * width
    
    # Create an empty output grid with the calculated dimensions, filled with zeros (or any default background color)
    # The dtype should match the input grid's data type
    output_np = np.zeros((height, output_width), dtype=int) 
    
    # --- Step 1: Copy the input grid to the left half of the output grid ---
    # Iterate through each row and column of the input grid
    # for r in range(height):
    #     for c in range(width):
    #         # Copy the pixel value to the same position in the output grid
    #         output_np[r, c] = input_np[r, c]
    # --- NumPy equivalent for Step 1 (more efficient) ---
    output_np[:, 0:width] = input_np
            
    # --- Step 2: Copy the horizontally reflected input grid to the right half ---
    # Iterate through each row and column of the input grid
    # for r in range(height):
    #     for c in range(width):
    #         # Calculate the corresponding reflected column index in the output grid
    #         # The reflection occurs across the vertical line at the right edge of the original input's position
    #         # Original column c maps to output column (output_width - 1 - c)
    #         reflected_c = (output_width - 1) - c 
    #         # Copy the pixel value from input[r, c] to output[r, reflected_c]
    #         output_np[r, reflected_c] = input_np[r, c]
    # --- NumPy equivalent for Step 2 (more efficient) ---
    # Create the horizontally flipped version of the input array
    reflected_input_np = np.fliplr(input_np)
    # Assign the reflected array to the right half of the output array
    output_np[:, width:output_width] = reflected_input_np

    # Convert the final NumPy array back to a list of lists for the return value
    output_grid = output_np.tolist()
    
    return output_grid