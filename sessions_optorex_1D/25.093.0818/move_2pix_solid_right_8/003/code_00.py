"""
Transforms a 1D input list of 12 integers by shifting all non-zero elements two positions to the right. Elements shifted beyond the list boundary are dropped. Positions vacated by the shift become 0.
"""

import numpy as np # Although not strictly necessary for lists, it's often available and might be useful if inputs change format

def transform(input_list):
    """
    Shifts all non-zero elements in a 1D list two positions to the right.

    Args:
      input_list: A list of 12 integers.

    Returns:
      A new list of 12 integers with non-zero elements shifted right by 2 positions.
    """
    # Define the length of the list (assumed to be 12 based on examples)
    n = 12 
    
    # Initialize an output list of the same length, filled with zeros.
    # This represents the background or default state.
    output_list = [0] * n

    # Iterate through the input list using index and value
    for i, element in enumerate(input_list):
        # Check if the current element is a non-zero element that needs shifting
        if element != 0:
            # Calculate the target index for the shift (2 positions to the right)
            target_index = i + 2

            # Check if the target index is within the bounds of the list (0 to n-1)
            if target_index < n:
                # Place the non-zero element into the output list at the shifted position
                output_list[target_index] = element
            # Else: if target_index >= n, the element is shifted out of bounds and is dropped (implicitly, as output_list remains 0 at indices beyond bounds)

    # Return the newly created list with shifted elements
    return output_list