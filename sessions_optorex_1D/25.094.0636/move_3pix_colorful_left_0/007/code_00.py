"""
Transform a sequence of 12 digits based on the following rules:

1.  Receive Input: Start with the input sequence, which is a list or array of 12 integer digits. Define constants: `sequence_length = 12`, `shift_amount = 3`.
2.  Find Start: Iterate through the input sequence from the beginning (index 0) to find the index of the first digit that is not 0. Let this index be `start_index`.
3.  Handle All Zeros: If no non-zero digit is found (`start_index` is -1), the output sequence is identical to the input sequence. Return a copy of the input sequence.
4.  Extract Block: If a non-zero digit is found at `start_index`, extract the `active_block`, which is the sub-sequence containing all elements of the input sequence from `start_index` to the end.
5.  Calculate New Position: Determine the target starting index for the `active_block` in the output: `new_start_index = start_index - shift_amount`. Ensure `new_start_index` is not less than 0 (set to 0 if the calculation results in a negative value).
6.  Construct Output Sequence: Create a new list (`result_sequence`) as follows:
    a.  Initialize `result_sequence` with `new_start_index` number of zeros.
    b.  Append all digits from the `active_block` to `result_sequence`.
    c.  Calculate the number of required trailing zeros: `trailing_zeros_count = sequence_length - len(result_sequence)`.
    d.  If `trailing_zeros_count` is positive, append that many zeros to `result_sequence`.
    e.  If `trailing_zeros_count` is negative (meaning the shifted block exceeded the length), truncate `result_sequence` to `sequence_length`.
7.  Return Output: Return the final `result_sequence`.
"""

import numpy as np # Use numpy for potential array operations and consistency

# Define constants used in the transformation
SEQUENCE_LENGTH = 12
SHIFT_AMOUNT = 3

def find_first_non_zero_index(sequence):
    """
    Helper function to find the index of the first non-zero element.

    Args:
        sequence: A list or NumPy array of numbers.

    Returns:
        The index of the first non-zero element, or -1 if none found.
    """
    for index, element in enumerate(sequence):
        if element != 0:
            return index
    return -1

def transform(input_sequence):
    """
    Applies the transformation rule to the input sequence of digits.

    Args:
        input_sequence: A list or NumPy array of 12 integers.

    Returns:
        A NumPy array representing the transformed sequence of 12 digits.
    """
    # Ensure input is handled as a NumPy array for consistency
    # Make a copy to avoid modifying the original input if it's mutable
    input_array = np.array(input_sequence).copy()

    # 2. Find Start: Find the index of the first non-zero digit.
    start_index = find_first_non_zero_index(input_array)

    # 3. Handle All Zeros: If no non-zero digit is found, return the input directly.
    if start_index == -1:
        return input_array # Return the original array (or a copy)

    # 4. Extract Block: Get the sub-sequence from start_index onwards.
    active_block = input_array[start_index:]

    # 5. Calculate New Position: Determine the target starting index, clamping at 0.
    new_start_index = max(0, start_index - SHIFT_AMOUNT)

    # 6. Construct Output Sequence:
    # a. Initialize with leading zeros. Use dtype from input.
    result_sequence = np.zeros(new_start_index, dtype=input_array.dtype)

    # b. Append the active block.
    result_sequence = np.concatenate((result_sequence, active_block))

    # c. & d. & e. Pad with trailing zeros or truncate to reach SEQUENCE_LENGTH.
    current_length = len(result_sequence)
    if current_length < SEQUENCE_LENGTH:
        # Append trailing zeros
        trailing_zeros_count = SEQUENCE_LENGTH - current_length
        trailing_zeros = np.zeros(trailing_zeros_count, dtype=input_array.dtype)
        result_sequence = np.concatenate((result_sequence, trailing_zeros))
    elif current_length > SEQUENCE_LENGTH:
        # Truncate if somehow the shifted block makes it too long
        result_sequence = result_sequence[:SEQUENCE_LENGTH]
    # else: length is already correct

    # 7. Return Output: Return the final sequence.
    return result_sequence