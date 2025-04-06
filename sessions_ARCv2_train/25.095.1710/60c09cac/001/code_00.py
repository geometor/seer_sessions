"""
Scales an input grid by a factor of 2. Each cell (r, c) in the input grid with 
value V is mapped to a 2x2 block of cells with value V in the output grid, 
starting at position (2*r, 2*c). The output grid dimensions are double the 
input grid dimensions.
"""

import numpy as np

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms an input grid by scaling it up by a factor of 2.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the scaled output grid.
    """
    # Convert input to numpy array for easier handling
    input_array = np.array(input_grid, dtype=int)
    
    # Determine the height (H) and width (W) of the input grid.
    input_height, input_width = input_array.shape

    # Calculate the dimensions for the output grid.
    output_height = input_height * 2
    output_width = input_width * 2

    # Create a new output grid initialized with zeros.
    # Using numpy.zeros ensures the correct data type.
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through each cell of the input grid.
    for r in range(input_height):
        for c in range(input_width):
            # Get the value V from the input cell at (r, c).
            value = input_array[r, c]
            
            # Calculate the top-left coordinates for the 2x2 block in the output grid.
            output_r = r * 2
            output_c = c * 2
            
            # Fill the 2x2 block in the output grid with the value V.
            output_grid[output_r    , output_c    ] = value
            output_grid[output_r + 1, output_c    ] = value
            output_grid[output_r    , output_c + 1] = value
            output_grid[output_r + 1, output_c + 1] = value

    # Convert the numpy array back to a list of lists for the return value.
    return output_grid.tolist()
