import numpy as np

"""
Rearranges a sequence of 12 numbers by swapping the first 8 elements with the last 4 elements.
The input is expected to be a 1D NumPy array or a list of numbers.
The output will be a list containing the rearranged sequence.
"""

def transform(input_sequence):
    """
    Transforms the input sequence by swapping the first 8 elements with the last 4.

    Args:
        input_sequence: A NumPy array or list containing 12 numbers.

    Returns:
        A list containing the transformed sequence of 12 numbers.
    """

    # Convert the input sequence to a list to ensure consistent slicing and concatenation
    input_list = list(input_sequence)

    # Optional: Validate input length (can be helpful for debugging)
    # if len(input_list) != 12:
    #     raise ValueError("Input sequence must contain exactly 12 elements.")

    # Identify the first segment: the first 8 elements (indices 0 through 7)
    segment_1 = input_list[:8]

    # Identify the second segment: the last 4 elements (indices 8 through 11)
    segment_2 = input_list[8:]

    # Construct the output sequence by concatenating segment_2 followed by segment_1
    output_sequence = segment_2 + segment_1

    # Return the transformed sequence as a list
    return output_sequence