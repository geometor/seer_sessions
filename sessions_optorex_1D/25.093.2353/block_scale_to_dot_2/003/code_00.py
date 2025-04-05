import numpy as np

"""
Accept the input, which is a sequence (list or array) of 12 integers.
Create a modifiable copy of the input sequence.
Locate the index of the number `2` (the marker) within the sequence.
Left Fill Process:
  Search backwards from the index immediately preceding the marker towards the beginning of the sequence.
  Identify the first non-zero number encountered (this is the `left_fill_value`) and record its index (`left_fill_index`).
  If a `left_fill_value` is found, iterate through the indices strictly between `left_fill_index` and the marker's index. Replace any element at these indices that is `0` with the `left_fill_value`.
Right Fill Process:
  Search forwards from the index immediately following the marker towards the end of the sequence.
  Identify the first non-zero number encountered (this is the `right_fill_value`) and record its index (`right_fill_index`).
  If a `right_fill_value` is found, iterate through the indices strictly between the marker's index and `right_fill_index`. Replace any element at these indices that is `0` with the `right_fill_value`.
Return the modified sequence.
"""

def find_first_occurrence(sequence, value):
    """Helper function to find the first index of a value in a sequence."""
    try:
        # np.where returns a tuple of arrays, one for each dimension.
        # For a 1D array, we take the first element of the tuple,
        # and then the first element of that array.
        indices = np.where(sequence == value)[0]
        if len(indices) > 0:
            return indices[0]
        else:
            return -1 # Indicate not found
    except Exception: # Catch potential errors if input isn't array-like or value not present
        return -1

def transform(input_sequence):
    """
    Applies a fill operation on a sequence of integers based on the position of the number 2.
    Zeros between the number 2 and the nearest non-zero numbers on either side are filled
    with those respective non-zero numbers.
    
    Args:
        input_sequence (numpy.ndarray): A 1D numpy array of 12 integers.

    Returns:
        numpy.ndarray: The modified numpy array.
    """
    # Ensure input is a numpy array and create a modifiable copy
    if not isinstance(input_sequence, np.ndarray):
        input_sequence = np.array(input_sequence)
    output_sequence = np.copy(input_sequence)
    n = len(output_sequence)

    # 1. Locate the index of the number 2 (the marker)
    marker_index = find_first_occurrence(output_sequence, 2)

    # If 2 is not found (shouldn't happen based on examples, but good practice)
    if marker_index == -1:
        return output_sequence # Return original if 2 is missing

    # 2. Left Fill Process
    left_fill_value = 0
    left_fill_index = -1
    # Search backwards from marker_index - 1 to index 0
    for i in range(marker_index - 1, -1, -1):
        if output_sequence[i] != 0:
            left_fill_value = output_sequence[i]
            left_fill_index = i
            break # Found the closest non-zero to the left

    # If a left fill value was found, fill the zeros between it and the marker
    if left_fill_index != -1:
        # Iterate from the index *after* the fill value up to (not including) the marker
        for i in range(left_fill_index + 1, marker_index):
            if output_sequence[i] == 0:
                output_sequence[i] = left_fill_value

    # 3. Right Fill Process
    right_fill_value = 0
    right_fill_index = -1
    # Search forwards from marker_index + 1 to the end of the sequence
    for i in range(marker_index + 1, n):
        if output_sequence[i] != 0:
            right_fill_value = output_sequence[i]
            right_fill_index = i
            break # Found the closest non-zero to the right

    # If a right fill value was found, fill the zeros between the marker and it
    if right_fill_index != -1:
        # Iterate from the index *after* the marker up to (not including) the fill value
        for i in range(marker_index + 1, right_fill_index):
             if output_sequence[i] == 0:
                output_sequence[i] = right_fill_value

    # 4. Return the modified sequence
    return output_sequence