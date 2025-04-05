import math
import collections
import numpy as np # Keep numpy import in case the final environment uses it, though the direct implementation uses lists.

"""
Transforms a string of space-separated binary digits (0s and 1s) into a list of integers (0s, 1s, and 3s).
The transformation rule is as follows: A '0' in the input sequence is changed to a '3' in the output list 
if and only if it is immediately adjacent (either to the left or right) to a sequence of exactly two 
consecutive '1's. This '1 1' sequence must be isolated, meaning it is not part of a longer sequence 
of '1's (e.g., '1 1 1'). '1's and '0's that do not meet this condition remain unchanged in the output list.
"""

def parse_input_string(input_str):
    """Parses a space-separated string of digits into a list of integers."""
    if not isinstance(input_str, str):
        # Adding a basic type check for robustness, although the prompt implies string input.
        raise TypeError("Input must be a string.")
    return [int(x) for x in input_str.split()]

def transform(input_str):
    """
    Applies the transformation rule to the parsed input sequence.

    Args:
        input_str: A string of space-separated binary digits (e.g., "1 0 0 1 1 0").

    Returns:
        A list of integers with '0's potentially replaced by '3's according 
        to the adjacency rule with isolated '1 1' sequences.
    """
    # Parse the input string into a list of integers
    input_list = parse_input_string(input_str)
    
    # Initialize output_list as a copy of the input list
    output_list = list(input_list)
    n = len(input_list)

    # Iterate through the input list with index
    for i in range(n):
        # Check only if the current element is 0
        if input_list[i] == 0:
            
            # Flag to track if the 0 needs to be changed to 3
            change_needed = False

            # --- Condition 1: Check if the '0' is immediately to the RIGHT of an isolated '1 1' ---
            # Pattern: [... 0/Start] [1 at i-2] [1 at i-1] [0 at i] ...
            
            # Check bounds (need indices i-1 and i-2)
            if i >= 2:
                # Check for '1 1' immediately to the left
                if input_list[i-1] == 1 and input_list[i-2] == 1:
                    # Check for isolation on the left side of '1 1'
                    # It's isolated if it's at the start (i==2) OR the element before '1 1' is 0 (at index i-3)
                    if i == 2 or input_list[i-3] == 0:
                        change_needed = True # Found the pattern to the left

            # --- Condition 2: Check if the '0' is immediately to the LEFT of an isolated '1 1' ---
            # Pattern: ... [0 at i] [1 at i+1] [1 at i+2] [0/End] ...

            # Check bounds (need indices i+1 and i+2)
            # Only proceed if change_needed is still False (avoid redundant checks/overwriting)
            if not change_needed and i <= n - 3: 
                 # Check for '1 1' immediately to the right
                if input_list[i+1] == 1 and input_list[i+2] == 1:
                    # Check for isolation on the right side of '1 1'
                    # It's isolated if it's near the end (i == n-3) OR the element after '1 1' is 0 (at index i+3)
                    if i == n - 3 or input_list[i+3] == 0:
                        change_needed = True # Found the pattern to the right
            
            # Apply the change if either condition was met
            if change_needed:
                output_list[i] = 3
        
        # If input_list[i] is 1, it remains unchanged in the output_list (due to initial copy)

    # Return the modified list
    return output_list