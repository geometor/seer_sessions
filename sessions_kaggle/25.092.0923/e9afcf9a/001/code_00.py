"""
Transforms a 2-row input grid where each row is monochromatic into a 2-row output grid of the same dimensions. The output grid's rows contain alternating sequences of the two input colors. 
Row 1 starts with the color from input row 1 and alternates with the color from input row 2.
Row 2 starts with the color from input row 2 and alternates with the color from input row 1.
"""

import numpy as np

def transform(input_grid):
    """
    Applies the alternating color pattern transformation to a 2-row input grid.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid. 
                                 Expected to have 2 rows, each monochromatic.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed output grid.
    """
    # Convert input_grid to numpy array if it isn't already
    input_grid_np = np.array(input_grid)
    
    # Get dimensions of the input grid
    height, width = input_grid_np.shape
    
    # Check if the input grid has exactly 2 rows
    if height != 2:
        # Or handle this case differently, e.g., return input or raise error
        print("Warning: Input grid does not have 2 rows. Returning input.") 
        return input_grid_np 

    # Identify the color of the first row (color1)
    # Assumes the first pixel represents the color of the entire row
    color1 = input_grid_np[0, 0] 
    
    # Identify the color of the second row (color2)
    # Assumes the first pixel represents the color of the entire row
    color2 = input_grid_np[1, 0]

    # Initialize the output grid with the same shape, filled with zeros initially
    output_grid = np.zeros_like(input_grid_np)

    # Fill the first row of the output grid (index 0)
    for j in range(width):
        if j % 2 == 0:  # Even column index
            output_grid[0, j] = color1
        else:           # Odd column index
            output_grid[0, j] = color2

    # Fill the second row of the output grid (index 1)
    for j in range(width):
        if j % 2 == 0:  # Even column index
            output_grid[1, j] = color2
        else:           # Odd column index
            output_grid[1, j] = color1

    return output_grid
