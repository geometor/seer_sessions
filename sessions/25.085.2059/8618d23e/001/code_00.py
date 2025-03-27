"""
Splits the input grid horizontally into two halves, places them diagonally in a 
larger grid (one row taller, one column wider), and fills the separating space 
with maroon (9). The top half goes to the top-left, the bottom half goes to the 
bottom-right relative section, shifted down and right. An 'L' shape of maroon 
pixels separates the two halves.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the described rule.

    Args:
        input_grid (list of lists int): The input grid represented as a list of lists.

    Returns:
        list of lists int: The transformed output grid.
    """
    # Convert input to numpy array for easier slicing and manipulation
    input_np = np.array(input_grid, dtype=int)
    H, W = input_np.shape

    # Calculate the midpoint row index (assuming even height based on examples)
    mid_row = H // 2

    # Determine the dimensions of the output grid
    output_H = H + 1
    output_W = W + 1

    # Create the output grid, initialized entirely with maroon (9)
    # This simplifies filling the gaps later.
    output_np = np.full((output_H, output_W), 9, dtype=int)

    # Identify the top and bottom halves of the input grid
    top_half = input_np[0:mid_row, :]
    bottom_half = input_np[mid_row:H, :]

    # Copy the top half to the top-left corner of the output grid
    # This overwrites the initial maroon values in that region.
    output_np[0:mid_row, 0:W] = top_half

    # Copy the bottom half to the bottom-right relative section of the output grid
    # This also overwrites the initial maroon values in that region.
    # Starts at row mid_row + 1 and column 1.
    output_np[mid_row + 1 : H + 1, 1 : W + 1] = bottom_half

    # The remaining parts of the output grid (middle row, parts of first and last columns)
    # were already initialized to maroon (9), so no further filling is needed.

    # Convert the numpy array back to a list of lists for the expected output format
    output_grid = output_np.tolist()

    return output_grid
