"""
Transforms an input sequence of digits by identifying the contiguous segment 
that starts with the first non-zero digit and ends with the last non-zero digit. 
This entire segment is then shifted 3 positions to the left within a new sequence 
of the same original length, initially filled with zeros. If the calculated 
left shift would result in a start index less than 0, the segment starts at index 0. 
If the input sequence contains only zeros, the output is also a sequence of zeros 
of the same length. The function handles list or 1D NumPy array inputs and returns a Python list.
"""

import numpy as np

def _find_first_nonzero_index(data):
    """Finds the index of the first non-zero element using NumPy."""
    non_zero_indices = np.nonzero(data)[0]
    if len(non_zero_indices) == 0:
        return -1 # Indicate no non-zero element found
    return non_zero_indices[0]

def _find_last_nonzero_index(data):
    """Finds the index of the last non-zero element using NumPy."""
    non_zero_indices = np.nonzero(data)[0]
    if len(non_zero_indices) == 0:
        return -1 # Indicate no non-zero element found
    return non_zero_indices[-1]

def transform(input_sequence):
    """
    Applies the described segment-shifting transformation.

    Args:
        input_sequence: A list or 1D NumPy array of integers.

    Returns:
        A list of integers representing the transformed sequence.
    """
    # Convert input to NumPy array for efficient processing, ensure it's 1D
    input_arr = np.array(input_sequence).flatten()
    n = len(input_arr)

    # Initialize the output list with zeros
    output_list = [0] * n

    # Find the start and end indices of the segment containing non-zero numbers
    start_index = _find_first_nonzero_index(input_arr)
    end_index = _find_last_nonzero_index(input_arr)

    # If no non-zero elements exist (start_index is -1), return the list of zeros
    if start_index == -1:
        return output_list

    # Extract the segment (including any zeros within the non-zero boundaries)
    # Ensure indices are valid before slicing
    if start_index <= end_index:
        segment = input_arr[start_index : end_index + 1]
        segment_len = len(segment)
    else:
        # This case should not be reachable if start_index != -1, but added for safety
        return output_list 

    # Calculate the target start index for the segment in the output
    # Shift amount is 3 to the left, ensuring it doesn't go below index 0
    target_start_index = max(0, start_index - 3)

    # Place the segment into the output list at the target position
    # Calculate how many elements of the segment can actually be placed
    elements_to_place = min(segment_len, n - target_start_index)
    
    # Copy the relevant part of the segment to the output list
    for i in range(elements_to_place):
        # Use standard list indexing for assignment
        output_list[target_start_index + i] = segment[i].item() # .item() converts numpy int to standard python int

    return output_list