"""
Transforms an input sequence of 12 integers by shifting the elements one position to the right, 
inserting a 0 at the beginning, and discarding the last element of the original sequence.
"""

import numpy as np # Although not strictly necessary for this specific task, it's good practice for grid/array manipulations

def transform(input_sequence):
    """
    Shifts the input sequence one position to the right, prepends a 0, 
    and removes the last element.

    Args:
        input_sequence (list): A list of 12 integers.

    Returns:
        list: The transformed list of 12 integers.
    """
    
    # Validate input length (optional but good practice)
    if len(input_sequence) != 12:
        raise ValueError("Input sequence must have exactly 12 elements.")

    # Take the first 11 elements from the input sequence (effectively discarding the last one)
    truncated_sequence = input_sequence[:-1] 
    
    # Create the output sequence by prepending 0 to the truncated sequence
    output_sequence = [0] + truncated_sequence
    
    return output_sequence
