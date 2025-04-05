"""
The transformation rule takes a sequence of 12 integers and performs a circular left rotation by 3 positions.
The first 3 elements of the input sequence are moved to the end of the sequence, and the elements from index 3 onwards are shifted to the beginning.
"""

import numpy as np
from typing import List, Union

def transform(input_sequence: Union[List[int], np.ndarray]) -> Union[List[int], np.ndarray]:
    """
    Performs a circular left shift by 3 positions on a sequence of 12 integers.

    Args:
        input_sequence: A list or numpy array containing 12 integers.

    Returns:
        A list or numpy array containing the transformed 12 integers.
    """

    # Ensure input is a list for easier slicing and concatenation
    # If it's already a list, this doesn't change it. If it's a NumPy array, it converts it.
    input_list = list(input_sequence) 

    # Define the number of positions to shift (rotate left)
    shift_amount = 3

    # Check if the input list has the expected length (optional, defensive programming)
    if len(input_list) != 12:
        # Depending on environment, might raise error or handle differently
        print(f"Warning: Input sequence length is {len(input_list)}, expected 12.") 
        # Attempt to proceed anyway if possible, or could raise ValueError

    # Perform the circular left rotation using list slicing
    # Part 1: Elements from the shift point to the end
    part1 = input_list[shift_amount:]
    
    # Part 2: Elements from the beginning up to the shift point
    part2 = input_list[:shift_amount]
    
    # Concatenate the two parts to create the rotated sequence
    output_sequence = part1 + part2

    # If the original input was a NumPy array, return a NumPy array
    # Otherwise, return a list
    if isinstance(input_sequence, np.ndarray):
        return np.array(output_sequence)
    else:
        return output_sequence