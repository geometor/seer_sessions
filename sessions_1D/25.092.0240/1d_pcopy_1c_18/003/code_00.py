import numpy as np

"""
Transforms a 1D array based on a specific pattern:
1. Find the first occurrence of a sequence of three identical non-white elements (C C C).
2. Identify the color (C) and the end index of this sequence.
3. Find all subsequent elements in the array that have the same color C (Trigger Pixels).
4. For each Trigger Pixel found at index 'j', change the elements at indices 'j-1' and 'j+1' to color C, provided these indices are within the array bounds.
5. Return the modified array.
"""

def find_first_ccc_pattern(arr):
    """
    Finds the first sequence of three identical non-white elements.

    Args:
        arr (np.array): The 1D input array.

    Returns:
        tuple: (color, end_index) if found, otherwise (None, -1).
               color is the value of the repeated element.
               end_index is the index of the third element in the sequence.
    """
    arr_len = len(arr)
    # Iterate up to the third-to-last element to allow checking i, i+1, i+2
    for i in range(arr_len - 2):
        color = arr[i]
        # Check if non-white (not 0) and if the next two elements are the same
        if color != 0 and arr[i+1] == color and arr[i+2] == color:
            # Found the first CCC pattern
            return color, i + 2
    # No CCC pattern found
    return None, -1

def transform(input_grid):
    """
    Applies the described transformation rule to the input grid (treated as 1D).

    Args:
        input_grid (list of lists): The input grid, expected to be 1xN.

    Returns:
        list of lists: The transformed grid, also 1xN.
    """
    # Ensure input is treated as a 1D array from the first row
    if not input_grid or not input_grid[0]:
        return input_grid # Handle empty or invalid input
        
    input_arr = np.array(input_grid[0], dtype=int)
    output_arr = np.copy(input_arr) # Create a copy to modify
    arr_len = len(output_arr)

    # Find the first C C C pattern
    ccc_color, ccc_end_index = find_first_ccc_pattern(input_arr)

    # If a pattern was found
    if ccc_color is not None:
        # Iterate through the array starting *after* the CCC pattern
        for j in range(ccc_end_index + 1, arr_len):
            # Check if the current element is a Trigger Pixel (matches the CCC color)
            if input_arr[j] == ccc_color:
                # Modify the element before the trigger pixel, if index is valid
                if j - 1 >= 0:
                    output_arr[j - 1] = ccc_color
                # Modify the element after the trigger pixel, if index is valid
                if j + 1 < arr_len:
                    output_arr[j + 1] = ccc_color

    # Return the modified array in the expected list of lists format
    return [output_arr.tolist()]