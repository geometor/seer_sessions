"""
Takes an input sequence of 12 integers. Performs a right shift operation on the 
entire sequence by 4 positions. Prepends 4 zeros to the beginning of the 
shifted sequence. Keeps only the first 12 elements of the resulting sequence, 
discarding any elements shifted beyond the 12th position. The resulting 
sequence of 12 integers is the output.
"""

import numpy as np

def transform(input_sequence_str: str) -> str:
    """
    Applies a right shift of 4 positions to the input sequence, padding with zeros.

    Args:
        input_sequence_str: A string representing the space-separated sequence of 12 integers.

    Returns:
        A string representing the space-separated transformed sequence of 12 integers.
    """
    # Parse the input string into a list of integers
    input_list = [int(x) for x in input_sequence_str.split()]

    # Define shift parameters
    shift_amount = 4
    fill_value = 0
    sequence_length = 12

    # Create the padding sequence
    padding = [fill_value] * shift_amount

    # Determine the part of the input sequence to keep
    # Elements from index 0 up to (but not including) sequence_length - shift_amount
    elements_to_keep = input_list[:sequence_length - shift_amount]

    # Construct the output sequence by prepending padding
    output_list = padding + elements_to_keep

    # Ensure the output list has the correct length (it should already, but as a safeguard)
    # This step is technically handled by the slicing and concatenation logic above
    # for this specific problem where length is fixed and shift amount is constant.
    # output_list = output_list[:sequence_length] 

    # Format the output list back into a space-separated string
    output_sequence_str = " ".join(map(str, output_list))

    return output_sequence_str
