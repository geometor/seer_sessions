"""
Transforms a sequence of 12 integers. It identifies the first non-zero integer ('active_digit') 
in the input sequence. It then initializes an output sequence as a copy of the input. 
It iterates through the input sequence from index 3 to 10. If an element at index 'i' 
in the input matches the 'active_digit', it sets the elements at indices i-1, i, and i+1 
in the output sequence to the 'active_digit'. Finally, it returns the modified output sequence.
"""

import math # Note: math is not strictly needed here, but included as per template guidance.
import numpy as np # Import numpy for potential array operations if input is array-like

# Helper function to find the first non-zero digit (active_digit)
def find_active_digit(sequence):
    """ Finds the first non-zero digit in the sequence. """
    for digit in sequence:
        if digit != 0:
            return digit
    return None # Return None if all digits are zero

def transform(input_sequence):
    """
    Applies the transformation rule to the input sequence.
    """
    # Ensure input is a list, handling potential NumPy array input
    if isinstance(input_sequence, np.ndarray):
        input_list = input_sequence.tolist()
    elif isinstance(input_sequence, str): # Handle string input case explicitly
        input_list = [int(x) for x in input_sequence.split()]
    else:
        input_list = list(input_sequence) # Assume it's already list-like or convert

    # Check sequence length
    if len(input_list) != 12:
        raise ValueError("Input sequence must have exactly 12 elements.")

    # Initialize the output sequence as a modifiable copy of the input
    output_sequence = list(input_list)

    # Identify the non-zero "active digit" using the helper function
    active_digit = find_active_digit(input_list)

    # If no active digit is found (input is all zeros), return the original sequence unchanged.
    if active_digit is None:
        return output_sequence # Return as list (or potentially convert back if needed)

    # Iterate through the *input* sequence indices where a trigger might occur.
    # The rule applies for triggers at index i > 2 (indices 3 to 10).
    # This range ensures indices i-1 (min 2) and i+1 (max 11) are valid for a length-12 list.
    for i in range(3, 11):
        # Check if the element at the current index 'i' in the *original input* sequence
        # matches the identified active digit.
        if input_list[i] == active_digit:
            # If a trigger is found, modify the *output* sequence.
            # Set the elements at index i-1, i, and i+1 to the active digit.
            # Index boundary checks (i-1 >= 0 and i+1 < 12) are implicitly handled by the loop range 3-10.
            output_sequence[i - 1] = active_digit
            output_sequence[i] = active_digit
            output_sequence[i + 1] = active_digit

    # Return the modified output sequence
    return output_sequence
