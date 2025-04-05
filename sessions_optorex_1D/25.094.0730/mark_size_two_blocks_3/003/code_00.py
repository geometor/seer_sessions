import math
import collections
import numpy as np # Import numpy, just in case the input is an array as suggested by the error message

"""
Transforms a list or 1D array of binary digits (0s and 1s) based on the following rule:
A '0' in the input is changed to a '3' in the output if and only if 
it is immediately adjacent (either to the left or right) to a sequence of 
exactly two consecutive '1's. This '1 1' sequence must be isolated, meaning 
it is not part of a longer sequence of '1's (e.g., '1 1 1'). 
'1's and '0's that do not meet this condition remain unchanged.
"""

def transform(input_sequence):
    """
    Applies the transformation rule to the input sequence.

    Args:
        input_sequence: A list or 1D numpy array of integers (0s and 1s).

    Returns:
        A new list with '0's potentially replaced by '3's according 
        to the adjacency rule with isolated '1 1' sequences.
    """
    # Handle potential numpy array input by converting to list
    if isinstance(input_sequence, np.ndarray):
        # Ensure it's 1D before converting
        if input_sequence.ndim > 1:
             raise ValueError("Input must be a 1D sequence (list or numpy array)")
        input_list = input_sequence.tolist()
    elif isinstance(input_sequence, list):
        input_list = input_sequence
    else:
        raise TypeError("Input must be a list or a 1D numpy array")

    # Initialize output_list as a copy of the input list
    output_list = list(input_list)
    n = len(input_list)

    # Iterate through the input list with index
    for i in range(n):
        # Check only if the current element is 0
        if input_list[i] == 0:
            
            # Flag to check if conditions are met to change 0 to 3
            change_to_3 = False

            # --- Condition 1: Check if the '0' is immediately to the RIGHT of an isolated '1 1' ---
            # Pattern: [... 0/Start] [1] [1] [0 at index i] ...
            
            # Check bounds (need indices i-1 and i-2)
            if i >= 2:
                # Check for '1 1' immediately to the left
                if input_list[i-1] == 1 and input_list[i-2] == 1:
                    # Check for isolation on the left side of '1 1'
                    # It's isolated if it's at the start (i==2) OR the element before '1 1' is 0 (at index i-3)
                    if i == 2 or input_list[i-3] == 0:
                        change_to_3 = True # Found the pattern to the left

            # --- Condition 2: Check if the '0' is immediately to the LEFT of an isolated '1 1' ---
            # Pattern: ... [0 at index i] [1] [1] [0/End] ...

            # Check bounds (need indices i+1 and i+2)
            # Only check if we haven't already decided to change based on the left condition
            if not change_to_3 and i <= n - 3: 
                 # Check for '1 1' immediately to the right
                if input_list[i+1] == 1 and input_list[i+2] == 1:
                    # Check for isolation on the right side of '1 1'
                    # It's isolated if it's near the end (i == n-3) OR the element after '1 1' is 0 (at index i+3)
                    if i == n - 3 or input_list[i+3] == 0:
                        change_to_3 = True # Found the pattern to the right
            
            # If either condition was met, change the output element to 3
            if change_to_3:
                output_list[i] = 3
        
        # If input_list[i] is 1, it remains unchanged (already handled by copying)

    # Return the modified list
    return output_list