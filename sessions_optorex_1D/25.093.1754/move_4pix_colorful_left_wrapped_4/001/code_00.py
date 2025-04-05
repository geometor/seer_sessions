"""
Takes a sequence of 12 integers and performs a cyclic left shift (rotation) 
on the sequence by 4 positions. The resulting sequence is the output.
"""

import collections

def transform(input_list):
    """
    Performs a 4-position left cyclic shift on the input list.

    Args:
        input_list: A list of 12 integers.

    Returns:
        A new list representing the input list shifted left by 4 positions.
    """
    
    # Ensure the input is a list (or can be treated like one)
    # and has the expected length, although the logic works for any length > shift_amount
    if not isinstance(input_list, list):
      # Attempt to convert if it's a common sequence type like tuple
      try:
        input_list = list(input_list)
      except TypeError:
        raise ValueError("Input must be a list or convertible to a list.")
        
    n = len(input_list)
    shift_amount = 4

    # Handle cases where list length might be smaller than shift amount, though not expected based on examples
    if n == 0:
        return []
    
    # Calculate the effective shift amount in case shift_amount >= n
    effective_shift = shift_amount % n 

    # Slice the list: take elements from the shift_amount index to the end
    first_part = input_list[effective_shift:]
    
    # Slice the list: take elements from the beginning up to the shift_amount index
    second_part = input_list[:effective_shift]
    
    # Concatenate the parts to create the shifted list
    output_list = first_part + second_part
    
    return output_list
