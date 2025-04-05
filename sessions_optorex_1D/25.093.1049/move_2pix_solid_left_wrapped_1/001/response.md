```python
import math

"""
Perform a circular left shift by 2 positions on the non-zero elements 
of a 12-element integer list. Zeros act as empty placeholders, and only 
non-zero elements are moved. The shift wraps around the ends of the list.
"""

def transform(input_list):
    """
    Transforms the input list by shifting non-zero elements circularly left by 2 positions.

    Args:
        input_list: A list of 12 integers.

    Returns:
        A new list of 12 integers with non-zero elements shifted.
    """
    # Define the length of the list (fixed at 12)
    list_length = 12
    
    # Initialize the output list with 12 zeros
    output_list = [0] * list_length

    # Iterate through the input list with index and value
    for i, value in enumerate(input_list):
        # Check if the current element is non-zero
        if value != 0:
            # Calculate the new index after shifting left by 2
            # Use the modulo operator (%) to handle wrap-around correctly
            # Python's % handles negative numbers as expected for circular shifts
            # e.g., (0 - 2) % 12 = -2 % 12 = 10
            # e.g., (1 - 2) % 12 = -1 % 12 = 11
            new_index = (i - 2) % list_length
            
            # Place the non-zero value at the calculated new index in the output list
            output_list[new_index] = value

    # Return the transformed list
    return output_list

```