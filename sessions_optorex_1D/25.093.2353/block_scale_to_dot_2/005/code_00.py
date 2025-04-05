import numpy as np

"""
The transformation operates on a sequence of 12 integers. It identifies the position of the number 2, which serves as a marker. It then finds the nearest non-zero integer to the left of the marker and the nearest non-zero integer to the right of the marker. Zeros located strictly between the left non-zero integer and the marker are replaced with the value of the left non-zero integer. Similarly, zeros located strictly between the marker and the right non-zero integer are replaced with the value of the right non-zero integer. If no non-zero integer exists on either side, no filling occurs on that side.
"""

def find_first_occurrence(sequence, value, start_index=0, end_index=None, reverse=False):
    """
    Helper function to find the first index of a value in a sequence within a specified range.
    Can search forwards or backwards.

    Args:
        sequence (list): The list to search within.
        value: The value to search for.
        start_index (int): The starting index for the search.
        end_index (int): The ending index (exclusive) for the search. Defaults to sequence length.
        reverse (bool): If True, searches backwards from end_index-1 down to start_index.

    Returns:
        int: The index of the first occurrence, or -1 if not found.
    """
    if end_index is None:
        end_index = len(sequence)

    if not reverse:
        indices = range(start_index, end_index)
    else:
        indices = range(end_index - 1, start_index - 1, -1)

    for i in indices:
        if sequence[i] == value:
            return i
    return -1

def find_first_non_zero(sequence, start_index=0, end_index=None, reverse=False):
    """
    Helper function to find the index and value of the first non-zero element
    in a sequence within a specified range. Can search forwards or backwards.

    Args:
        sequence (list): The list to search within.
        start_index (int): The starting index for the search.
        end_index (int): The ending index (exclusive) for the search. Defaults to sequence length.
        reverse (bool): If True, searches backwards from end_index-1 down to start_index.

    Returns:
        tuple: (index, value) of the first non-zero element, or (-1, 0) if none found.
    """
    if end_index is None:
        end_index = len(sequence)

    if not reverse:
        indices = range(start_index, end_index)
    else:
        # Search from end_index-1 down to start_index
        indices = range(end_index - 1, start_index - 1, -1)

    for i in indices:
        if sequence[i] != 0:
            return i, sequence[i]
    return -1, 0 # Indicate not found


def transform(input_sequence):
    """
    Applies a fill operation on a sequence of integers based on the position of the number 2.
    Zeros between the number 2 and the nearest non-zero numbers on either side are filled
    with those respective non-zero numbers.

    Args:
        input_sequence (list): A list of 12 integers.

    Returns:
        list: The modified list of integers.
    """
    # Ensure we're working with a list and create a modifiable copy
    if isinstance(input_sequence, np.ndarray):
        # Convert numpy array to list if necessary
        output_sequence = input_sequence.tolist()
    elif isinstance(input_sequence, str):
         # Convert string input to list
         output_sequence = [int(x) for x in input_sequence.split()]
    else:
         # Assume it's already a list-like object, make a copy
        output_sequence = list(input_sequence)
        
    n = len(output_sequence)

    # 1. Locate the index of the number 2 (the marker)
    marker_index = find_first_occurrence(output_sequence, 2)

    # If 2 is not found (edge case, shouldn't happen based on examples)
    if marker_index == -1:
        return output_sequence # Return original if 2 is missing

    # 2. Left Fill Process
    # Search backwards from marker_index - 1 down to index 0
    left_fill_index, left_fill_value = find_first_non_zero(output_sequence, 
                                                          start_index=0, 
                                                          end_index=marker_index, 
                                                          reverse=True)

    # If a left fill value was found, fill the zeros between it and the marker
    if left_fill_index != -1:
        # Iterate from the index *after* the fill value up to (not including) the marker
        for i in range(left_fill_index + 1, marker_index):
            if output_sequence[i] == 0:
                output_sequence[i] = left_fill_value

    # 3. Right Fill Process
    # Search forwards from marker_index + 1 to the end of the sequence
    right_fill_index, right_fill_value = find_first_non_zero(output_sequence, 
                                                             start_index=marker_index + 1, 
                                                             end_index=n, 
                                                             reverse=False)

    # If a right fill value was found, fill the zeros between the marker and it
    if right_fill_index != -1:
        # Iterate from the index *after* the marker up to (not including) the fill value
        for i in range(marker_index + 1, right_fill_index):
             if output_sequence[i] == 0:
                output_sequence[i] = right_fill_value

    # 4. Return the modified sequence
    return output_sequence