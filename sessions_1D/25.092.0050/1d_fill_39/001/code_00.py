import numpy as np
import math

"""
Identify the non-white color and the indices of the two pixels containing this color in the input 1D grid. 
Determine the minimum and maximum of these two indices. Create an output grid of the same size, 
initially all white (0). Fill the segment in the output grid from the minimum index to the maximum 
index (inclusive) with the identified non-white color.
"""

def find_non_white_pixels(grid_row):
    """Finds the color and indices of non-white pixels in a 1D grid row."""
    non_white_color = 0
    indices = []
    for index, pixel_value in enumerate(grid_row):
        if pixel_value != 0:
            # Assuming only one non-white color exists per the examples
            non_white_color = pixel_value 
            indices.append(index)
    # The problem statement implies exactly two such pixels
    if len(indices) != 2:
        # Handle potential errors or unexpected input formats if necessary
        # For this specific task based on examples, we assume 2 indices are found.
        # If not, the min/max logic below might fail or produce incorrect results.
        # print(f"Warning: Expected 2 non-white pixels, found {len(indices)}")
        pass 
    return non_white_color, indices

def transform(input_grid):
    """
    Transforms the input 1D grid by filling the segment between the two 
    non-white pixels with their color.
    
    Args:
        input_grid (list): A list containing a single list representing the 1D grid. 
                           Example: [[0, 0, 8, 0, 0, 8, 0]]

    Returns:
        list: A list containing a single list representing the transformed 1D grid.
              Example: [[0, 0, 8, 8, 8, 8, 0]]
    """
    # Ensure input is treated as a 1D array/list
    # The ARC standard provides grids as list of lists, even for 1D
    if not isinstance(input_grid, list) or len(input_grid) != 1 or not isinstance(input_grid[0], list):
         raise ValueError("Input grid must be a list containing a single list (1D row).")
         
    input_row = input_grid[0]
    grid_width = len(input_row)

    # 1. Identify the non-white color and its indices
    fill_color, indices = find_non_white_pixels(input_row)

    # Check if exactly two indices were found (as expected from examples)
    if len(indices) != 2:
        # If not exactly two markers, return the input unchanged or handle error
        # Based on the examples, this case shouldn't occur for valid inputs.
        # Returning a copy to avoid modifying original input if needed.
        return [row[:] for row in input_grid] 

    # 2. Determine the segment boundaries (min and max index)
    min_index = min(indices)
    max_index = max(indices)

    # 3. Create the output grid, initialized to white (0)
    output_row = [0] * grid_width

    # 4. Fill the segment in the output grid with the fill color
    for i in range(min_index, max_index + 1):
        output_row[i] = fill_color
        
    # 5. Return the output grid in the standard ARC format (list of lists)
    return [output_row]
