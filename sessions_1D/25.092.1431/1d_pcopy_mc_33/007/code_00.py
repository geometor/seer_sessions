import copy
import numpy as np # numpy might be useful for grid operations, though not strictly necessary here

"""
Transforms a single-row grid by identifying non-white pixels 'C' that are surrounded by two white pixels on each side (pattern: 0, 0, C, 0, 0). 
For each such pattern found in the input grid, the central three pixels (0, C, 0) at indices [i-1, i, i+1] are replaced by (C, C, C) in the output grid at the same indices. 
Pixels not involved in this specific 5-pixel pattern context and subsequent transformation are copied directly from the input to the output.
"""

def find_isolated_pixel_markers(input_row):
    """
    Finds all occurrences of the pattern (0, 0, C, 0, 0) where C is non-zero.

    Args:
        input_row (list): The single row of the input grid.

    Returns:
        list: A list of tuples, where each tuple contains the index (i) 
              of the central non-white pixel 'C' and the color 'C' itself.
              e.g., [(index1, color1), (index2, color2), ...]
    """
    markers = []
    width = len(input_row)
    # Iterate through possible center indices 'i' for the 5-pixel pattern
    # Need i-2 and i+2 to be valid indices, so range is [2, width-3]
    for i in range(2, width - 2):
        center_pixel = input_row[i]
        # Check the pattern: 0, 0, C (non-zero), 0, 0
        if center_pixel != 0 and \
           input_row[i-2] == 0 and \
           input_row[i-1] == 0 and \
           input_row[i+1] == 0 and \
           input_row[i+2] == 0:
            markers.append((i, center_pixel)) # Store index and color
    return markers

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list of lists): A 2D list representing the input grid. 
                                     Expected to have only one row.

    Returns:
        list of lists: A 2D list representing the transformed output grid.
    """
    # === Input Validation ===
    if not isinstance(input_grid, list) or not input_grid or not all(isinstance(row, list) for row in input_grid):
        print("Warning: Invalid input format. Expected list[list[int]]. Returning input.")
        # Consider raising TypeError for stricter handling
        return copy.deepcopy(input_grid) 

    if len(input_grid) != 1:
        print("Warning: Expected single-row grid based on examples. Processing only the first row.")
        # Decide if this is an error or acceptable behavior based on requirements
        
    input_row = input_grid[0]
    width = len(input_row)

    # Handle edge case: row too short to contain the 5-pixel pattern
    if width < 5:
        # Return an unmodified copy as no transformation is possible
        return copy.deepcopy(input_grid) 

    # === Initialization ===
    # Create the output row as a copy of the input row.
    # Modifications will be made to this copy based on patterns found in the original input_row.
    output_row = list(input_row) # Shallow copy is sufficient

    # === Find Patterns ===
    # Find all locations where the transformation trigger pattern exists in the *input* row
    markers_to_transform = find_isolated_pixel_markers(input_row)

    # === Apply Transformations ===
    # Iterate through the identified markers and modify the *output* row
    for index, color in markers_to_transform:
        # The pattern (0, 0, C, 0, 0) is centered at 'index'.
        # We need to modify the pixels at index-1, index, and index+1 in the output row.
        output_row[index - 1] = color
        output_row[index]     = color
        output_row[index + 1] = color

    # === Return Result ===
    # Return the modified row wrapped in a list to maintain the grid structure [[]].
    return [output_row]