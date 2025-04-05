import numpy as np # Although not strictly necessary for list slicing/concatenation, import it in case the input is a numpy array.

"""
Rearranges a sequence of 12 numbers by swapping the first 8 elements with the last 4 elements.
"""

def transform(input_sequence):
    """
    Transforms the input sequence by swapping the first 8 elements with the last 4.

    Args:
        input_sequence: A list or NumPy array containing 12 numbers.

    Returns:
        A new list containing the transformed sequence of 12 numbers.
    """

    # Ensure the input is treated as a list for consistent slicing and concatenation
    # This handles both standard lists and NumPy arrays gracefully.
    input_list = list(input_sequence) 
    
    # Validate input length (optional but good practice)
    if len(input_list) != 12:
        raise ValueError("Input sequence must contain exactly 12 elements.")

    # Identify the first segment (first 8 elements, indices 0 through 7)
    segment_1 = input_list[:8]

    # Identify the second segment (last 4 elements, indices 8 through 11)
    segment_2 = input_list[8:]

    # Construct the output sequence by concatenating segment_2 followed by segment_1
    output_sequence = segment_2 + segment_1

    # Return the transformed sequence
    return output_sequence