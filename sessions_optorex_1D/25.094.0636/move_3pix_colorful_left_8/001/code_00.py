"""
Performs a cyclic left shift on a sequence of 12 space-separated digits by 3 positions.
The first 3 digits are moved to the end of the sequence in their original order, 
and all other digits are shifted 3 positions to the left.
"""

import collections

def transform(input_str: str) -> str:
    """
    Applies a cyclic left shift of 3 positions to the input sequence string.

    Args:
        input_str: A string containing 12 space-separated digits.

    Returns:
        A string representing the sequence after the cyclic left shift, 
        with digits separated by spaces.
    """
    # Parse the input string into a list of digits (as strings)
    digits = input_str.split()

    # Check if the input has the expected length (optional but good practice)
    if len(digits) != 12:
        # Handle error or unexpected input appropriately
        # For this task, we assume valid input based on examples
        pass 

    # Define the shift amount
    shift_amount = 3

    # Perform the cyclic left shift
    # Take the elements from the shift_amount index to the end
    shifted_part = digits[shift_amount:]
    # Take the elements from the beginning up to the shift_amount index
    wrapped_part = digits[:shift_amount]
    # Concatenate them in the new order
    output_digits = shifted_part + wrapped_part

    # Format the output list back into a space-separated string
    output_str = " ".join(output_digits)

    return output_str
