"""
Transforms an input sequence of 12 digits by shifting all non-zero digits 4 positions to the right.

1. Receive the input sequence of 12 digits.
2. Create a new output sequence of 12 digits, initialized with all zeros.
3. Iterate through the input sequence from left to right (index 0 to 11).
4. For each element in the input sequence:
    a. If the element is not zero:
        i. Calculate the target index in the output sequence by adding 4 to the current element's index.
        ii. Place the non-zero element at this target index in the output sequence.
5. Return the completed output sequence.
"""

import numpy as np

def transform(input_sequence):
    """
    Shifts non-zero elements in a sequence 4 positions to the right.

    Args:
        input_sequence: A list or numpy array of 12 integers.

    Returns:
        A list of 12 integers representing the transformed sequence.
    """
    # Determine the length of the sequence
    sequence_length = len(input_sequence)
    
    # Initialize the output sequence with zeros
    output_sequence = [0] * sequence_length 
    
    # Define the shift amount
    shift_amount = 4

    # Iterate through the input sequence with index
    for index, element in enumerate(input_sequence):
        # Check if the element is non-zero
        if element != 0:
            # Calculate the new index after shifting
            new_index = index + shift_amount
            # Ensure the new index is within the bounds of the sequence
            if 0 <= new_index < sequence_length:
                # Place the non-zero element at the new index in the output sequence
                output_sequence[new_index] = element
                
    return output_sequence
