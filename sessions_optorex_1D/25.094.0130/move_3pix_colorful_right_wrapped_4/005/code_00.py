"""
Transforms an input sequence of 12 integers by performing a right circular shift by 3 positions.
This moves the last 3 elements to the beginning of the sequence.
"""

import numpy as np  # Import numpy as input might be an array

def transform(input_sequence):
    """
    Performs a right circular shift by 3 positions on the input sequence.

    Args:
        input_sequence: A list or numpy array containing 12 integers.

    Returns:
        A list or numpy array containing the transformed sequence of 12 integers,
        maintaining the input type if it was a numpy array.
    """

    # Ensure the input sequence has the expected length (optional check)
    if len(input_sequence) != 12:
        raise ValueError("Input sequence must contain exactly 12 elements.")

    # Slice the input sequence to get the last 3 elements.
    last_three = input_sequence[-3:]

    # Slice the input sequence to get the first 9 elements.
    first_nine = input_sequence[:-3]

    # Construct the output sequence by concatenating the last three elements
    # followed by the first nine elements.
    # Convert slices to lists to ensure standard concatenation works,
    # especially if the input was a numpy array where '+' might mean element-wise addition.
    output_sequence_list = list(last_three) + list(first_nine)

    # Check if the original input was a numpy array.
    # If so, convert the output list back to a numpy array to maintain type consistency.
    if isinstance(input_sequence, np.ndarray):
        output_sequence = np.array(output_sequence_list, dtype=input_sequence.dtype)
    else:
        # Otherwise, return the result as a standard list.
        output_sequence = output_sequence_list

    # Return the transformed sequence.
    return output_sequence