"""
Fill the horizontal gap between two identical non-white pixels in a single-row grid.

1. Receive the input grid (expected as a list of lists, representing 1 row).
2. Extract the single row.
3. Find the indices and colors of all non-white pixels (value > 0) in the row.
4. Check if exactly two non-white pixels were found.
5. If two were found, check if they have the same color value.
6. If both conditions are met (count=2, same color):
    a. Determine the fill color.
    b. Find the minimum (start) and maximum (end) indices.
    c. Create a copy of the original row.
    d. Fill the segment between start and end (inclusive) in the copied row with the fill color.
    e. Return the modified row packaged as a list of lists.
7. If conditions are not met, return the original input grid unchanged.
"""

import numpy as np
import copy

def transform(input_grid):
    """
    Fills the horizontal gap between two identical non-white pixels in a single row grid.

    Args:
        input_grid (list): A list containing a single list representing the input grid row. 
                           Example: [[0, 0, 4, 0, 4, 0]]

    Returns:
        list: A list containing a single list representing the transformed output grid row.
              Returns the original input_grid if the transformation conditions are not met.
    """
    
    # Check if the input grid structure is valid (list containing one list)
    if not isinstance(input_grid, list) or len(input_grid) != 1 or not isinstance(input_grid[0], list):
        # Or handle error appropriately if strict validation is needed
        return copy.deepcopy(input_grid) # Return original if format is unexpected

    # Extract the single row
    input_row = input_grid[0]
    
    # Use numpy for efficient searching, but operate on list copy for output if needed
    input_array = np.array(input_row)
    
    # Find the indices of the non-white pixels (values > 0)
    non_white_indices = np.where(input_array > 0)[0] # np.where returns a tuple

    # Initialize output_grid as a deep copy of the input_grid
    # This ensures we return the original structure if conditions aren't met
    output_grid = copy.deepcopy(input_grid)

    # Check condition 1: Exactly two non-white pixels found
    if len(non_white_indices) == 2:
        idx1, idx2 = non_white_indices[0], non_white_indices[1]
        color1 = input_array[idx1]
        color2 = input_array[idx2]

        # Check condition 2: The two non-white pixels have the same color
        if color1 == color2:
            # Conditions met, perform the transformation
            fill_color = color1
            start_index = min(idx1, idx2)
            end_index = max(idx1, idx2)

            # Modify the row within the output_grid list structure
            output_row = output_grid[0] # Get the list representing the row
            for i in range(start_index, end_index + 1):
                 # Check index bounds just in case, although unlikely needed here
                if 0 <= i < len(output_row):
                    output_row[i] = fill_color
            # The modification happens in-place on the list within output_grid

            return output_grid # Return the modified grid

    # If conditions (count != 2 or colors differ) are not met, return the original grid copy
    return output_grid