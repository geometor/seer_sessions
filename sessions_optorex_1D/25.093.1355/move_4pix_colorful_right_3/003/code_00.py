import math
# numpy is available, but not strictly needed for this list manipulation
# import numpy as np 
import re 

"""
Transforms an input sequence of 12 integers by shifting its elements 4 positions to the right. 
Elements shifted off the right end are discarded. 
The 4 leftmost positions are filled with zeros.
The input is received as a sequence (e.g., list or numpy array), not a string.
"""

def transform(input_sequence):
    """
    Applies a right shift of 4 positions to the input sequence.

    Args:
        input_sequence: A sequence (list or numpy array) containing 12 integers.

    Returns:
        A list containing the transformed 12 integers.
    """
    # Define constants based on observed pattern
    shift_amount = 4
    sequence_length = 12

    # Ensure input is a list for consistent handling, 
    # though direct array manipulation is also possible if input is guaranteed to be numpy array.
    # This handles both list and numpy array inputs.
    input_list = list(input_sequence) 

    # Initialize the output list with zeros
    # This handles the left padding implicitly
    output_list = [0] * sequence_length

    # Iterate through the input list indices that will have a corresponding
    # position in the output list after shifting.
    # Only elements from input index 0 to sequence_length - shift_amount - 1
    # will end up in the output.
    for i in range(sequence_length - shift_amount):
        # Calculate the target index in the output list
        target_index = i + shift_amount
        
        # Assign the input element to the corresponding shifted position in the output list
        output_list[target_index] = input_list[i]

    # Alternative iteration: iterate through all input elements and check bounds
    # for i in range(sequence_length):
    #     target_index = i + shift_amount
    #     if target_index < sequence_length:
    #         output_list[target_index] = input_list[i]

    # Return the resulting transformed list
    return output_list