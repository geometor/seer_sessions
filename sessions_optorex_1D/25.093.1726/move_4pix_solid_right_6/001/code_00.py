import numpy as np

"""
Transforms a 12-element sequence by shifting all non-zero elements 4 positions to the right.
Positions vacated by the shift and any new positions at the beginning are filled with zeros.
Elements shifted beyond the end of the sequence are discarded.
"""

def transform(input_sequence_str):
    """
    Applies the right shift transformation to the input sequence.

    Args:
        input_sequence_str: A string representing the input sequence, with numbers separated by spaces.

    Returns:
        A string representing the transformed sequence, with numbers separated by spaces.
    """
    # Parse the input string into a list of integers
    input_sequence = [int(x) for x in input_sequence_str.split()]
    sequence_length = 12 # The length is fixed at 12 based on examples

    # Initialize the output sequence with zeros
    output_sequence = [0] * sequence_length

    # Iterate through the input sequence
    for i in range(sequence_length):
        # Check if the current element is non-zero
        if input_sequence[i] != 0:
            # Calculate the target index after shifting 4 positions to the right
            target_index = i + 4

            # Check if the target index is within the bounds of the sequence
            if 0 <= target_index < sequence_length:
                # Assign the non-zero value to the target position in the output sequence
                output_sequence[target_index] = input_sequence[i]

    # Convert the output list back to a space-separated string
    output_sequence_str = " ".join(map(str, output_sequence))
    return output_sequence_str
