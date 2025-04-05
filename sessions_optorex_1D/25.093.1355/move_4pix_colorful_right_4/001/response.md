```python
"""
Transforms an input sequence of 12 integers by shifting its elements 4 positions to the right. The first 4 positions of the output sequence are filled with 0. Elements shifted beyond the 12th position from the input sequence are discarded.
"""

import numpy as np

def transform(input_sequence_str: str) -> str:
    """
    Shifts the elements of an integer sequence to the right.

    Args:
        input_sequence_str: A string containing 12 space-separated integers.

    Returns:
        A string containing the transformed 12 space-separated integers.
    """
    # Parse the input string into a list of integers
    input_list = [int(x) for x in input_sequence_str.split()]
    
    # Define the shift amount
    shift_amount = 4
    
    # Define the fill value
    fill_value = 0
    
    # Define the length of the sequence
    sequence_length = 12
    
    # Create the prefix of zeros
    # This list will contain 'shift_amount' number of 'fill_value' elements
    prefix = [fill_value] * shift_amount
    
    # Select the elements from the input sequence that will be kept
    # These are the first 'sequence_length - shift_amount' elements
    elements_to_keep = input_list[:sequence_length - shift_amount]
    
    # Construct the output sequence by concatenating the prefix and the kept elements
    output_list = prefix + elements_to_keep
    
    # Format the output list back into a space-separated string
    output_sequence_str = " ".join(map(str, output_list))
    
    return output_sequence_str

```