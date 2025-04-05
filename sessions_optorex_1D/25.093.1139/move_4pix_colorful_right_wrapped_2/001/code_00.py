"""
Performs a right cyclic shift on a sequence of 12 integers by 4 positions.
The last 4 elements of the input sequence become the first 4 elements of the
output sequence, and the first 8 elements of the input sequence become the
last 8 elements of the output sequence.
"""

import numpy as np # numpy is commonly used for array manipulations

def transform(input_sequence):
    """
    Applies a right cyclic shift of 4 positions to the input sequence.

    Args:
        input_sequence (list or np.array): A sequence of 12 integers.

    Returns:
        list: The transformed sequence after the cyclic shift.
    """
    # Define the amount to shift
    shift_amount = 4
    
    # Ensure input is a list or easily convertible (like a numpy array)
    if isinstance(input_sequence, np.ndarray):
        input_sequence = input_sequence.tolist()
        
    # Check if the input sequence length is as expected (optional but good practice)
    if len(input_sequence) != 12:
        # Handle error or unexpected length if necessary
        # For this task, we assume length is always 12 based on examples
        pass 

    # Identify the last 'shift_amount' elements
    last_elements = input_sequence[-shift_amount:]
    
    # Identify the first 'length - shift_amount' elements
    first_elements = input_sequence[:-shift_amount]
    
    # Construct the output sequence by concatenating the parts
    # The last elements come first, followed by the first elements
    output_sequence = last_elements + first_elements
    
    return output_sequence
