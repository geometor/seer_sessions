"""
Combine the top and bottom halves of the input grid.
The output grid has the same width as the input but half the height.
An output cell (r, c) is set to yellow (4) if the corresponding cell in the top half of the input grid (r, c) is green (3) OR the corresponding cell in the bottom half of the input grid (r + input_height/2, c) is gray (5).
Otherwise, the output cell remains white (0).
"""

import numpy as np

def transform(input_grid):
    """
    Applies the described transformation rule to the input grid.

    Args:
        input_grid (list of lists or numpy array): The input grid.

    Returns:
        numpy array: The transformed output grid.
    """
    # Convert input to numpy array for easier slicing and element access
    input_array = np.array(input_grid, dtype=int)
    
    # Get dimensions of the input grid
    input_height, input_width = input_array.shape
    
    # Calculate the height of the output grid (half of the input height)
    output_height = input_height // 2
    output_width = input_width
    
    # Initialize the output grid with white (0) pixels
    output_grid = np.zeros((output_height, output_width), dtype=int)
    
    # Iterate through each cell coordinate (r, c) for the output grid
    for r in range(output_height):
        for c in range(output_width):
            # Get the color from the corresponding cell in the top half of the input
            top_half_color = input_array[r, c]
            
            # Get the color from the corresponding cell in the bottom half of the input
            # The row index in the input is r + output_height (which is input_height / 2)
            bottom_half_color = input_array[r + output_height, c]
            
            # Check if the top half cell is green (3) or the bottom half cell is gray (5)
            if top_half_color == 3 or bottom_half_color == 5:
                # If either condition is true, set the output cell to yellow (4)
                output_grid[r, c] = 4
            # Otherwise, the output cell remains white (0) as initialized
            
    return output_grid.tolist() # Convert back to list of lists if required by the environment
