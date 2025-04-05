```python
import numpy as np # Using numpy for array handling might be convenient, but list operations are sufficient

"""
The transformation operates on a sequence of 12 integers. It identifies the position 
of the number 2, which serves as a marker. It then finds the nearest non-zero 
integer to the left of the marker and the nearest non-zero integer to the right 
of the marker. Zeros located strictly between the left non-zero integer and the 
marker are replaced with the value of the left non-zero integer. Similarly, zeros 
located strictly between the marker and the right non-zero integer are replaced 
with the value of the right non-zero integer. If no non-zero integer exists on 
either side of the marker within the sequence bounds, no filling occurs on that respective side.
"""

# --- Helper Functions ---

def find_first_occurrence(sequence, value, start_index=0, end_index=None, reverse=False):
    """
    Finds the index of the first occurrence of a value in a list within a specified range.
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

    # Determine the range of indices to iterate over based on search direction
    if not reverse:
        indices = range(start_index, end_index)
    else:
        # Search backwards: from end_index-1 down to start_index (inclusive)
        indices = range(end_index - 1, start_index - 1, -1)

    # Iterate and return index if value is found
    for i in indices:
        # Check boundary conditions (although range should handle this)
        if 0 <= i < len(sequence):
             if sequence[i] == value:
                return i
    return -1 # Value not found in the specified range

def find_first_non_zero(sequence, start_index=0, end_index=None, reverse=False):
    """
    Finds the index and value of the first non-zero element in a list within a specified range.
    Can search forwards or backwards.

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

    # Determine the range of indices to iterate over based on search direction
    if not reverse:
        indices = range(start_index, end_index)
    else:
        # Search backwards: from end_index-1 down to start_index (inclusive)
        indices = range(end_index - 1, start_index - 1, -1)

    # Iterate and return index/value if non-zero is found
    for i in indices:
         # Check boundary conditions (although range should handle this)
        if 0 <= i < len(sequence):
            if sequence[i] != 0:
                return i, sequence[i]
    return -1, 0 # Indicate non-zero not found

# --- Main Transformation Function ---

def transform(input_sequence):
    """
    Applies the fill transformation based on the marker '2'.

    Args:
        input_sequence (list or similar iterable): A sequence of 12 integers.

    Returns:
        list: The modified list of integers.
    """
    # 1. Ensure input is a list and create a modifiable copy
    # Handles potential numpy array or string inputs gracefully
    if isinstance(input_sequence, np.ndarray):
        output_sequence = input_sequence.tolist()
    elif isinstance(input_sequence, str):
         output_sequence = [int(x) for x in input_sequence.split()]
    else:
        output_sequence = list(input_sequence) # Make a copy

    n = len(output_sequence)

    # 2. Locate the index of the marker '2'
    marker_index = find_first_occurrence(output_sequence, 2)

    # Handle edge case where marker '2' is not found (though unlikely based on examples)
    if marker_index == -1:
        return output_sequence # Return original sequence if no marker

    # 3. Left Fill Process
    #    a. Search backwards from marker_index-1 down to 0 for the first non-zero
    left_fill_index, left_fill_value = find_first_non_zero(output_sequence,
                                                          start_index=0,
                                                          end_index=marker_index, # Search up to (not including) marker
                                                          reverse=True)

    #    b. If a left fill value is found, fill zeros between it and the marker
    if left_fill_index != -1:
        # Iterate strictly between left_fill_index and marker_index
        for i in range(left_fill_index + 1, marker_index):
            if output_sequence[i] == 0:
                output_sequence[i] = left_fill_value

    # 4. Right Fill Process
    #    a. Search forwards from marker_index+1 to the end for the first non-zero
    right_fill_index, right_fill_value = find_first_non_zero(output_sequence,
                                                             start_index=marker_index + 1, # Start search after marker
                                                             end_index=n,
                                                             reverse=False)

    #    b. If a right fill value is found, fill zeros between the marker and it
    if right_fill_index != -1:
        # Iterate strictly between marker_index and right_fill_index
        for i in range(marker_index + 1, right_fill_index):
             if output_sequence[i] == 0:
                output_sequence[i] = right_fill_value

    # 5. Return the modified sequence
    return output_sequence
```