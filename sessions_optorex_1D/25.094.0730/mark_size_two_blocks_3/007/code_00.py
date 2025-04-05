import math
import collections
import numpy as np # Including numpy as it's often available, though not strictly needed for this list-based logic.

"""
Transforms a list of binary integers (0s and 1s) into a list of integers (0s, 1s, and 3s).
The transformation rule is: A '0' in the input list is changed to a '3' in the output list 
if and only if it is immediately adjacent (either to the left or right) to a sequence of 
exactly two consecutive '1's. This '1 1' sequence must be isolated, meaning it is not part 
of a longer sequence of '1's (e.g., '1 1 1'). '1's and '0's that do not meet this 
condition remain unchanged in the output list.
"""

def transform(input_list):
    """
    Applies the transformation rule to the input list.

    Args:
        input_list: A list of integers (0s and 1s).

    Returns:
        A new list with '0's potentially replaced by '3's according 
        to the adjacency rule with isolated '1 1' sequences.
    """
    
    # Ensure input is a list, handle potential numpy array input if necessary
    # (Based on previous iterations, sticking to list processing seems appropriate)
    if not isinstance(input_list, list):
        # If it's a numpy array, convert it. Otherwise, raise error.
        if isinstance(input_list, np.ndarray) and input_list.ndim == 1:
             input_list = input_list.tolist()
        else:
            # Raise error for unexpected types or dimensions
             raise TypeError("Input must be a list or a 1D numpy array of integers.")

    # Initialize output_list as a copy of the input list
    output_list = list(input_list)
    n = len(input_list)

    # Iterate through the input list with index
    for i in range(n):
        # Check only if the current element is 0, as 1s are never changed
        if input_list[i] == 0:
            
            # Flag to track if the 0 needs to be changed to 3
            change_needed = False

            # --- Condition A: Check if the '0' is immediately to the LEFT of an isolated '1 1' ---
            # Pattern: ... [0 at i] [1 at i+1] [1 at i+2] [0/End] ...
            
            # Check bounds (need indices i+1, i+2, and potentially i+3 for isolation check)
            if i <= n - 3: 
                 # Check for '1 1' immediately to the right
                if input_list[i+1] == 1 and input_list[i+2] == 1:
                    # Check for isolation on the right side of '1 1'
                    # It's isolated if it's near the end (i == n-3, so no i+3 exists) 
                    # OR the element after '1 1' is 0 (at index i+3)
                    if i == n - 3 or input_list[i+3] == 0:
                        change_needed = True # Found the pattern to the right

            # --- Condition B: Check if the '0' is immediately to the RIGHT of an isolated '1 1' ---
            # Pattern: [... 0/Start] [1 at i-2] [1 at i-1] [0 at i] ...
            
            # Check bounds (need indices i-1, i-2, and potentially i-3 for isolation check)
            # Only check this if Condition A wasn't already met
            if not change_needed and i >= 2:
                # Check for '1 1' immediately to the left
                if input_list[i-1] == 1 and input_list[i-2] == 1:
                    # Check for isolation on the left side of '1 1'
                    # It's isolated if it's at the start (i==2, so no i-3 exists) 
                    # OR the element before '1 1' is 0 (at index i-3)
                    if i == 2 or input_list[i-3] == 0:
                        change_needed = True # Found the pattern to the left
            
            # Apply the change if either condition was met
            if change_needed:
                output_list[i] = 3
        
        # If input_list[i] is 1, it remains unchanged in the output_list (due to initial copy)

    # Return the modified list
    return output_list