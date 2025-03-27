"""
Modify a single pixel in the input grid based on a color found in the top row.
The target pixel to modify is located in the last row and the middle column 
(specifically, column index floor(width / 2)). The color to set this target
pixel to is the color found in the first row (row 0) of the same middle column.
"""

import math
import copy

def transform(input_grid):
    """
    Transforms the input grid by changing one pixel in the last row.
    
    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed output grid.
    """
    
    # Get the dimensions of the input grid
    height = len(input_grid)
    if height == 0:
        return [] # Handle empty grid case
    width = len(input_grid[0])
    if width == 0:
        return [[] for _ in range(height)] # Handle grid with empty rows

    # Calculate the middle column index
    # Using floor division as specified in the observations
    mid_col = width // 2 
    
    # Calculate the last row index
    last_row = height - 1

    # Get the color of the source pixel (first row, middle column)
    source_color = input_grid[0][mid_col]

    # Create a deep copy of the input grid to avoid modifying the original
    # This ensures the input remains unchanged if needed elsewhere
    output_grid = copy.deepcopy(input_grid)

    # Modify the target pixel in the output grid (last row, middle column)
    # Set its color to the source_color
    output_grid[last_row][mid_col] = source_color

    # Return the modified grid
    return output_grid
