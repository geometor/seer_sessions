"""
Identifies the unique non-white color in the input 1D array.
Finds the first and last indices of this color.
Creates an output array by copying the input.
Fills the segment of the output array between the first and last indices (inclusive) with the identified non-white color.
"""

import numpy as np

def transform(input_grid):
    """
    Fills the segment between the first and last occurrences of a non-white color
    in a 1D array.

    Args:
        input_grid (list): A 1D list representing the input array of colors.

    Returns:
        list: A 1D list representing the transformed output array.
    """
    # Convert input list to a numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    
    # Initialize the output array as a copy of the input
    output_array = input_array.copy()

    # Find the unique non-white color(s)
    # Assuming there's only one non-white color based on examples
    non_white_pixels = input_array[input_array != 0]
    if len(non_white_pixels) == 0:
        # If the input is all white, return it unchanged
        return output_array.tolist()
        
    fill_color = non_white_pixels[0] # Get the first (and assumed only) non-white color

    # Find the indices where the fill_color appears
    indices = np.where(input_array == fill_color)[0]
    
    # Determine the start and end indices of the segment to fill
    if len(indices) >= 1: # Need at least one occurrence to define a segment (even if start=end)
        start_index = np.min(indices)
        end_index = np.max(indices)

        # Fill the segment in the output array
        # Iterate from start_index to end_index (inclusive)
        for i in range(start_index, end_index + 1):
            output_array[i] = fill_color

    # Convert the result back to a list before returning
    return output_array.tolist()
