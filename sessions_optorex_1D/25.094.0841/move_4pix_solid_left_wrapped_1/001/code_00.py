"""
Transforms an input sequence of 12 digits by performing a circular left shift of 4 positions.
Each digit in the input sequence at index `i` is moved to the index `(i - 4 + 12) % 12`
in the output sequence. Digits shifted off the beginning wrap around to the end.
"""

import collections

def transform(input_str: str) -> str:
    """
    Applies a circular left shift of 4 positions to the input sequence.

    Args:
        input_str: A string containing 12 space-separated digits.

    Returns:
        A string containing the transformed 12 space-separated digits.
    """
    # Parse the input string into a list of integers
    input_list = [int(digit) for digit in input_str.split()]
    
    # Define the length of the sequence and the shift amount
    n = len(input_list)
    shift_amount = 4

    # Use collections.deque for efficient rotation
    # Deque allows O(k) rotation where k is the shift amount
    d = collections.deque(input_list)
    
    # Perform a left circular shift (rotate with a negative value)
    d.rotate(-shift_amount) 
    
    # Convert the rotated deque back to a list
    output_list = list(d)
    
    # Format the output list back into a space-separated string
    output_str = " ".join(map(str, output_list))
    
    return output_str
