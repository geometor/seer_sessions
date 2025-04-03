import copy
import numpy as np # Though not strictly necessary for this logic, good practice for potential array ops

"""
Transforms a 1D input grid (row) by identifying isolated single non-white pixels 
and expanding each into a horizontal block of three pixels of the same color in 
the output grid. 

An isolated pixel is defined as a non-white pixel located between indices 1 and 
length-2 (inclusive) whose immediate left and right neighbors in the input grid 
have different colors than the pixel itself. The identification of isolated 
pixels is based solely on the original input grid. The expansion overwrites 
the pixels at indices i-1, i, and i+1 in the output grid, where i is the 
index of the isolated pixel in the input grid. Pixels not identified as 
isolated and not overwritten by an expansion retain their original input color.
"""

def _find_isolated_pixels(input_row):
    """
    Identifies isolated pixels in a single row based on the definition.
    
    Args:
        input_row (list[int]): The row to analyze.
        
    Returns:
        list[tuple[int, int]]: A list of tuples, where each tuple contains 
                                (index, color) of an identified isolated pixel.
    """
    isolated_pixels_info = []
    row_len = len(input_row)
    
    # Iterate through potential isolated pixel indices (1 to len-2)
    # We don't check index 0 or row_len - 1 as they cannot be isolated by definition.
    for i in range(1, row_len - 1):
        current_color = input_row[i]
        
        # Check if the pixel is non-white (not background color 0)
        if current_color == 0:
            continue
            
        # Get neighbor colors
        left_color = input_row[i - 1]
        right_color = input_row[i + 1]
        
        # Check if neighbors have different colors than the current pixel
        if left_color != current_color and right_color != current_color:
            # This pixel is isolated
            isolated_pixels_info.append((i, current_color))
            
    return isolated_pixels_info

def transform(input_grid):
    """
    Applies the isolated pixel expansion transformation to the input grid.
    """
    # --- Input Validation and Setup ---
    # Expect a grid containing exactly one row. Handle potential errors/edge cases.
    if not isinstance(input_grid, list) or len(input_grid) != 1 or not isinstance(input_grid[0], list):
        # Handle invalid input format - returning empty grid for now
        # ARC tasks usually guarantee valid input structure for examples/test cases.
        return [[]] 
        
    input_row = input_grid[0]
    row_len = len(input_row)

    # Handle empty row case
    if row_len == 0:
      return [[]]

    # --- Initialization ---
    # Create a modifiable copy of the input row to serve as the output row.
    # This ensures modifications don't affect subsequent identification steps.
    output_row = copy.deepcopy(input_row)

    # --- Identify Objects/Patterns ---
    # Find all pixels in the *original* input row that meet the "isolated" criteria.
    isolated_pixels = _find_isolated_pixels(input_row)

    # --- Apply Transformation ---
    # Iterate through the identified isolated pixels and modify the output row.
    for index, color in isolated_pixels:
        # Expand the isolated pixel into a 3-pixel block of the same color.
        # The _find_isolated_pixels function ensures 'index' is valid for neighbors.
        # Overwrite pixels at index-1, index, and index+1 in the output row.
        
        # Safely check boundaries although the find function restricts index range
        if index - 1 >= 0:
             output_row[index - 1] = color
        output_row[index] = color
        if index + 1 < row_len:
             output_row[index + 1] = color

    # --- Return Result ---
    # Wrap the modified row back into the grid format (list of lists).
    return [output_row]