"""
Transformation Rule:
Examine the first two elements of the input list. If both the first and second 
elements are 0, create the output list by taking the sub-list starting from 
the third element to the end of the input list and appending two 0s to the end. 
Otherwise, the output list is identical to the input list.
"""

import numpy as np # Although not strictly needed for list manipulation, it's often useful for grid/array tasks

def transform(input_list):
    """
    Applies the transformation rule to the input list.

    Args:
        input_list: A list of integers.

    Returns:
        A list of integers representing the transformed output.
    """

    # Check if the list has at least two elements
    if len(input_list) < 2:
        # If not, return the list as is (or a copy)
        return list(input_list)

    # Check if the first two elements are both 0
    if input_list[0] == 0 and input_list[1] == 0:
        # Create the output list by taking elements from the third position onwards
        output_list = input_list[2:]
        # Append two zeros to the end
        output_list.extend([0, 0])
        return output_list
    else:
        # If the first two elements are not both 0, return the list unchanged (return a copy)
        return list(input_list)
