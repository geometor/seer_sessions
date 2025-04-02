"""
Transforms a 1D array by identifying the unique non-white color, finding the 
first and last indices where this color appears, and then filling the entire 
segment between these two indices (inclusive) with that color. Pixels outside 
this segment remain unchanged. If the input contains no non-white pixels, it 
is returned unmodified.
"""

import numpy as np

def find_non_white_properties(input_array):
    """
    Finds the indices, color, min index, and max index of non-white pixels.

    Args:
        input_array (np.array): The input 1D numpy array.

    Returns:
        tuple: (non_white_indices, fill_color, start_index, end_index)
               Returns (None, None, None, None) if no non-white pixels are found.
    """
    # Find the indices of all pixels that are not white (0)
    non_white_indices = np.where(input_array != 0)[0]

    # Check if any non-white pixels were found
    if len(non_white_indices) == 0:
        return None, None, None, None
    else:
        # Determine the color (assume only one non-white color exists)
        fill_color = input_array[non_white_indices[0]]
        # Find the minimum and maximum indices
        start_index = np.min(non_white_indices)
        end_index = np.max(non_white_indices)
        return non_white_indices, fill_color, start_index, end_index

def transform(input_grid):
    """
    Transforms the input 1D array by filling the segment between the 
    first and last non-white pixel with that pixel's color.

    Args:
        input_grid (list): A 1D list representing the input array of colors.

    Returns:
        list: A 1D list representing the transformed output array.
    """
    # Convert input list to a numpy array for efficient operations
    input_array = np.array(input_grid, dtype=int)

    # Create the output array as an exact copy of the input array initially.
    output_array = input_array.copy()

    # Find properties of non-white pixels
    non_white_indices, fill_color, start_index, end_index = find_non_white_properties(input_array)

    # Check if non-white pixels were found
    if non_white_indices is not None:
        # If non-white pixels exist, fill the segment in the output array
        # Use array slicing for efficiency: set all elements from start_index
        # up to and including end_index to fill_color
        output_array[start_index : end_index + 1] = fill_color

    # Convert the result back to a standard Python list before returning
    return output_array.tolist()