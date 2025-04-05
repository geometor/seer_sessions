import math
import numpy as np
import re

"""
Transforms an input sequence of 12 space-separated integers by shifting its elements 4 positions to the right. 
Elements shifted off the right end are discarded. 
The 4 leftmost positions are filled with zeros.
"""

def parse_input(input_str):
    """Converts a space-separated string of integers into a list of integers."""
    return [int(x) for x in input_str.strip().split()]

def format_output(output_list):
    """Converts a list of integers into a space-separated string."""
    return " ".join(map(str, output_list))

def transform(input_str):
    """
    Applies a right shift of 4 positions to the input sequence.

    Args:
        input_str: A string containing 12 space-separated integers.

    Returns:
        A string containing the transformed 12 space-separated integers.
    """
    # Define constants
    shift_amount = 4
    length = 12

    # Parse the input string into a list of integers
    input_list = parse_input(input_str)
    
    # Validate input length (optional but good practice)
    if len(input_list) != length:
        # Handle error appropriately, e.g., raise ValueError or return an error indicator
        # For this task, we assume valid input length based on examples
        pass 

    # Initialize the output list with zeros
    output_list = [0] * length

    # Iterate through the input list to perform the shift
    for i in range(length):
        # Calculate the target index in the output list
        target_index = i + shift_amount
        
        # Check if the target index is within the bounds of the output list
        if target_index < length:
            # Assign the input element to the corresponding shifted position in the output list
            output_list[target_index] = input_list[i]

    # Format the output list back into a space-separated string
    output_str = format_output(output_list)

    return output_str
