"""
Overlays the top half and bottom half of the input grid using a logical XOR operation 
to determine the output grid pixels. Specifically, an output pixel is Magenta (6) 
if the corresponding pixel in the top half is Maroon (9) OR the corresponding pixel 
in the bottom half is Yellow (4), but not both. Otherwise, the output pixel is White (0).
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on an XOR-like comparison between its top and bottom halves.

    Args:
        input_grid (list of lists): A 2D list representing the input grid.

    Returns:
        list of lists: A 2D list representing the transformed output grid.
    """
    # Convert input to numpy array for easier slicing and manipulation
    input_array = np.array(input_grid, dtype=int)

    # Get the dimensions
    input_height, input_width = input_array.shape
    
    # Ensure the input height is even for splitting
    if input_height % 2 != 0:
        raise ValueError("Input grid height must be even to split into two halves.")

    # Calculate the height of the output grid (half the input height)
    output_height = input_height // 2
    output_width = input_width

    # Split the input grid into top and bottom halves
    top_half = input_array[:output_height, :]
    bottom_half = input_array[output_height:, :]

    # Initialize the output grid with White (0)
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through each cell position in the output grid dimensions
    for r in range(output_height):
        for c in range(output_width):
            # Get the pixel values from the corresponding positions in the top and bottom halves
            top_pixel = top_half[r, c]
            bottom_pixel = bottom_half[r, c]

            # Determine if the top pixel is Maroon (9)
            top_is_maroon = (top_pixel == 9)
            
            # Determine if the bottom pixel is Yellow (4)
            bottom_is_yellow = (bottom_pixel == 4)

            # Apply the XOR logic: if exactly one condition is true, set output to Magenta (6)
            if top_is_maroon ^ bottom_is_yellow: # XOR operator
                output_grid[r, c] = 6
            # Otherwise, it remains White (0) as initialized

    # Convert the output numpy array back to a list of lists for the expected format
    return output_grid.tolist()