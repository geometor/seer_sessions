"""
Identifies isolated foreground pixels (pattern '0 C 0') in a 1D input grid and replaces them with a block of three foreground pixels ('C C C').
The foreground color 'C' is the single non-white (non-zero) color present in the grid.
Pixels already part of a horizontal block of the foreground color are left unchanged.
The transformation preserves the grid dimensions.
"""

import numpy as np

def find_foreground_color(grid):
    """
    Finds the single non-white (non-zero) color in the grid.
    Assumes there is exactly one such color besides white (0).
    """
    unique_colors = np.unique(grid)
    for color in unique_colors:
        if color != 0:
            return color
    # Return a default or handle the case where only white is present
    # (though based on examples, a foreground color always exists)
    return None # Or raise an error if appropriate

def transform(input_grid):
    """
    Transforms the input grid according to the rule:
    Replace '0 C 0' with 'C C C', where C is the foreground color.
    """
    # Convert input list to numpy array for easier indexing and manipulation
    input_array = np.array(input_grid)
    output_array = input_array.copy() # Initialize output_grid as a copy

    # Get the dimensions (length) of the 1D grid
    grid_length = len(input_array)

    # Find the foreground color
    foreground_color = find_foreground_color(input_array)

    # If no foreground color is found (e.g., all white grid), return the original
    if foreground_color is None:
        return output_array.tolist() # Return as list to match input format if needed

    # Iterate through the grid, checking for the '0 C 0' pattern
    # We need to check indices i-1, i, and i+1, so the loop runs from 1 to length-2
    for i in range(1, grid_length - 1):
        # Check if the current pixel and its neighbors match the '0 C 0' pattern
        if (input_array[i - 1] == 0 and
            input_array[i] == foreground_color and
            input_array[i + 1] == 0):
            
            # Apply the transformation: change the neighbors and the pixel itself to 'C' in the output grid
            output_array[i - 1] = foreground_color
            output_array[i] = foreground_color
            output_array[i + 1] = foreground_color

    # Return the modified grid as a list
    return output_array.tolist()