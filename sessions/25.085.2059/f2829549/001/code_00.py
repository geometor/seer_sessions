"""
Transforms a 4x7 input grid into a 4x3 output grid based on a pixel-wise comparison across a central blue separator.

1.  Identifies a vertical blue line (color 1) at column index 3 which acts as a separator.
2.  Extracts the subgrid to the left of the separator (columns 0-2, `left_grid`).
3.  Extracts the subgrid to the right of the separator (columns 4-6, `right_grid`).
4.  Creates a new output grid with the dimensions of the subgrids (4x3), initialized to white (0).
5.  Iterates through each cell (r, c) of the subgrids.
6.  If the pixel at (r, c) in `left_grid` is white (0) AND the pixel at (r, c) in `right_grid` is white (0), sets the corresponding pixel (r, c) in the output grid to green (3).
7.  Otherwise, the output pixel remains white (0).
8.  Returns the resulting output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the output grid.
    """
    # Convert input grid to a numpy array for easier slicing
    input_np = np.array(input_grid, dtype=int)
    
    # Define colors and separator column index based on observations
    white_color = 0
    green_color = 3
    separator_col_index = 3 # Consistently blue (1) in column 3

    # Extract the left subgrid (columns 0 to separator_col_index - 1)
    left_grid = input_np[:, :separator_col_index]
    
    # Extract the right subgrid (columns separator_col_index + 1 to end)
    right_grid = input_np[:, separator_col_index + 1:]

    # Get the dimensions for the output grid (should match the subgrids)
    output_height, output_width = left_grid.shape
    
    # Initialize the output grid with white color (0)
    output_grid = np.full((output_height, output_width), white_color, dtype=int)

    # Iterate through each pixel of the subgrids
    for r in range(output_height):
        for c in range(output_width):
            # Get the corresponding pixel values from left and right grids
            left_pixel = left_grid[r, c]
            right_pixel = right_grid[r, c]
            
            # Apply the transformation rule
            # If both corresponding pixels in the left and right subgrids are white (0)
            if left_pixel == white_color and right_pixel == white_color:
                # Set the corresponding pixel in the output grid to green (3)
                output_grid[r, c] = green_color
                
    # Convert the numpy array back to a list of lists for the final output
    return output_grid.tolist()
