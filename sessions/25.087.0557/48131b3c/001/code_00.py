"""
Transforms an input grid by first swapping its two colors (white and one non-white color) 
and then tiling the resulting intermediate grid in a 2x2 arrangement to create an 
output grid twice the size in both dimensions.
"""

import numpy as np

def transform(input_grid):
    """
    Applies the color swap and 2x2 tiling transformation.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed output grid.
    """
    # Convert input_grid to numpy array if it's a list of lists
    input_grid_np = np.array(input_grid)
    
    # Identify the two colors present in the input grid
    unique_colors = np.unique(input_grid_np)
    white_color = 0
    non_white_color = [c for c in unique_colors if c != white_color][0]

    # Create the intermediate grid by swapping colors
    intermediate_grid = input_grid_np.copy()
    # Find where the colors are
    is_white = intermediate_grid == white_color
    is_non_white = intermediate_grid == non_white_color
    # Swap them
    intermediate_grid[is_white] = non_white_color
    intermediate_grid[is_non_white] = white_color

    # Get the dimensions of the intermediate grid
    input_height, input_width = intermediate_grid.shape

    # Calculate the dimensions of the output grid
    output_height = input_height * 2
    output_width = input_width * 2

    # Initialize the output grid with zeros (or any default value)
    output_grid = np.zeros((output_height, output_width), dtype=input_grid_np.dtype)

    # Tile the intermediate grid into the four quadrants of the output grid
    output_grid[0:input_height, 0:input_width] = intermediate_grid  # Top-left
    output_grid[0:input_height, input_width:output_width] = intermediate_grid  # Top-right
    output_grid[input_height:output_height, 0:input_width] = intermediate_grid  # Bottom-left
    output_grid[input_height:output_height, input_width:output_width] = intermediate_grid  # Bottom-right

    return output_grid