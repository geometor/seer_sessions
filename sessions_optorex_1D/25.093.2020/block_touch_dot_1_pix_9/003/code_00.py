"""
Transforms a sequence (list or array) of 12 integers based on specific patterns involving the numbers 0 and 2 near the end of the sequence.

1. If the second-to-last element (index n-2) is 0 and the last element (index n-1) is 2, move the 0 from the second-to-last position to the beginning (index 0) of the sequence.
2. If the third-to-last element (index n-3) is 2 and the second-to-last element (index n-2) is 0, move the 0 from the second-to-last position to the very end of the sequence.
3. Otherwise, the sequence remains unchanged.
"""

import numpy as np # Import numpy as it's commonly used and the error suggested it
import math
# Other potential imports if needed later:
# import re
# from collections import Counter

def transform(input_sequence):
    """
    Applies the transformation rule to the input sequence.

    Args:
        input_sequence: A list or numpy array of 12 integers.

    Returns:
        A list or numpy array representing the transformed sequence.
        (Returning a list is generally safer if the input type isn't guaranteed numpy)
    """
    # Convert input to a list to ensure mutable operations like pop, insert, append work as expected.
    # This handles both list and numpy array inputs.
    output_list = list(input_sequence)
    n = len(output_list)

    # Check Condition 1: Penultimate is 0 and Ultimate is 2
    # Indices are n-2 (10) and n-1 (11) for length 12
    # Ensure sequence is long enough for these indices
    if n >= 2 and output_list[n - 2] == 0 and output_list[n - 1] == 2:
        # Remove the 0 from the penultimate position
        value_to_move = output_list.pop(n - 2)
        # Insert the 0 at the beginning
        output_list.insert(0, value_to_move)
        # Return the modified list
        # If numpy array output is strictly required by the environment:
        # return np.array(output_list)
        return output_list

    # Check Condition 2: Antepenultimate is 2 and Penultimate is 0
    # Indices are n-3 (9) and n-2 (10) for length 12
    # Ensure sequence is long enough for these indices
    elif n >= 3 and output_list[n - 3] == 2 and output_list[n - 2] == 0:
        # Remove the 0 from the penultimate position
        value_to_move = output_list.pop(n - 2)
        # Append the 0 to the end
        output_list.append(value_to_move)
        # Return the modified list
        # If numpy array output is strictly required by the environment:
        # return np.array(output_list)
        return output_list

    # Otherwise (neither condition met):
    else:
        # Return the original sequence (or the unmodified copy)
        # If numpy array output is strictly required by the environment:
        # return np.array(output_list) # or just input_sequence if it was already np
        return output_list
