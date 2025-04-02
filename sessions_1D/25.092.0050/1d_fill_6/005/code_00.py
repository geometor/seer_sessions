"""
Fills the segment between the first and last occurrence of a non-white color 
in a 1D array, preserving pixels outside the segment. The input is assumed 
to contain at most one non-white color. If no non-white color exists, the 
input is returned unchanged.
"""

import numpy as np

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
    # Modifications will be made directly to this array.
    output_array = input_array.copy()

    # Find the indices of all pixels in the input array that are not white (0).
    non_white_indices = np.where(input_array != 0)[0]

    # Check if any non-white pixels were found.
    if len(non_white_indices) == 0:
        # If no non-white pixels are found, return the unmodified output array (copy of input).
        return output_array.tolist()
    else:
        # If non-white pixels are found:
        # a. Determine the color of these non-white pixels.
        #    We assume there's only one such color based on examples,
        #    so we take the color of the first non-white pixel found.
        fill_color = input_array[non_white_indices[0]]

        # b. Find the smallest index (position) where fill_color appears.
        start_index = np.min(non_white_indices)

        # c. Find the largest index (position) where fill_color appears.
        end_index = np.max(non_white_indices)

        # d. Modify the output array:
        #    Iterate through the indices from start_index to end_index (inclusive).
        for i in range(start_index, end_index + 1):
            # Set the color of the pixel at index i to fill_color.
            output_array[i] = fill_color

        # Return the modified output array, converted back to a list.
        return output_array.tolist()