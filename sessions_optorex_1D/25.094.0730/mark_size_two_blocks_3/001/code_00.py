import math
import collections

"""
Transforms a list of binary digits (0s and 1s) based on the following rule:
A '0' in the input list is changed to a '3' in the output list if and only if 
it is immediately adjacent (either to the left or right) to a sequence of 
exactly two consecutive '1's. '1's and '0's that do not meet this condition 
remain unchanged. Sequences of three or more consecutive '1's do not cause 
adjacent '0's to change.
"""

def transform(input_list):
    """
    Applies the transformation rule to the input list.

    Args:
        input_list: A list of integers (0s and 1s).

    Returns:
        A new list with '0's potentially replaced by '3's according 
        to the adjacency rule with '1 1' sequences.
    """
    # Initialize output_list as a copy of the input
    output_list = list(input_list)
    n = len(input_list)

    # Iterate through the input list with index
    for i in range(n):
        # Check only if the current element is 0
        if input_list[i] == 0:
            # Condition 1: Check if the '0' is to the right of an isolated '1 1'
            # Indices must be valid: i-1 >= 0, i-2 >= 0 => i >= 2
            # Must have '1 1' to the left: input_list[i-1] == 1 and input_list[i-2] == 1
            # Must NOT have a '1' before the '1 1': (i == 2) or (i > 2 and input_list[i-3] == 0)
            is_right_of_isolated_11 = False
            if i >= 2 and input_list[i-1] == 1 and input_list[i-2] == 1:
                if i == 2 or input_list[i-3] == 0:
                    is_right_of_isolated_11 = True

            # Condition 2: Check if the '0' is to the left of an isolated '1 1'
            # Indices must be valid: i+1 < n, i+2 < n => i <= n - 3
            # Must have '1 1' to the right: input_list[i+1] == 1 and input_list[i+2] == 1
            # Must NOT have a '1' after the '1 1': (i == n - 3) or (i < n - 3 and input_list[i+3] == 0)
            is_left_of_isolated_11 = False
            if i <= n - 3 and input_list[i+1] == 1 and input_list[i+2] == 1:
                if i == n - 3 or input_list[i+3] == 0:
                     is_left_of_isolated_11 = True
                     
            # If either condition is met, change the output element to 3
            if is_right_of_isolated_11 or is_left_of_isolated_11:
                output_list[i] = 3
        
        # If input_list[i] is 1, it remains unchanged (already handled by copying)

    return output_list
