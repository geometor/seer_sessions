"""
Transforms an input sequence of 12 integers by performing a left cyclic shift 
(or left rotation) of 2 positions. The first two elements of the input sequence 
are moved to the end, and all other elements shift two positions to the left.
"""

import numpy as np
from typing import List, Union, Sequence 

def transform(input_sequence: Sequence[int]) -> List[int]:
    """
    Applies a left cyclic shift of 2 positions to the input sequence.

    Args:
        input_sequence: A sequence (e.g., list or tuple) of 12 integers. 
                          Note: While the examples use 1D data, the template uses 
                          'input_grid', suggesting potential 2D data later. 
                          This implementation assumes a 1D sequence based on examples.

    Returns:
        A list representing the transformed sequence.
    """
    
    # Convert input sequence to a list to ensure mutability and consistent handling
    # (Handles lists, tuples, potentially 1D numpy arrays implicitly via iteration)
    input_list = list(input_sequence) 

    # Define the fixed number of positions for the left cyclic shift
    shift_amount = 2

    # Check if the list is long enough to perform the shift
    # (Basic safeguard, though examples guarantee length 12)
    if len(input_list) < shift_amount:
        # Handle edge case: if list is shorter than shift amount, return it as is or raise error
        # For this specific problem with fixed length 12, this might not be strictly needed
        # but is good practice for general functions. Returning as is for now.
        print(f"Warning: Input sequence length {len(input_list)} is less than shift amount {shift_amount}.")
        return input_list
        # Alternatively, could implement modulo arithmetic for shift_amount if inputs varied drastically
        # shift_amount = shift_amount % len(input_list) if len(input_list) > 0 else 0


    # Perform the left cyclic shift using list slicing
    
    # Extract the elements that will wrap around from the beginning
    wrapped_part = input_list[:shift_amount]
    
    # Extract the elements that will shift to the beginning
    shifted_part = input_list[shift_amount:]
    
    # Concatenate the shifted part and the wrapped part to form the output sequence
    output_list = shifted_part + wrapped_part

    # Return the transformed list
    return output_list
