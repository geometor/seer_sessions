import math
import collections
import itertools
import numpy as np # Import numpy as the error message suggests it might be involved

"""
Transforms a sequence of integers (0s and 1s) by changing certain 0s to 3s.
A 0 is changed to a 3 if it is immediately preceded by two 1s OR immediately
followed by two 1s. Otherwise, elements retain their original values.
Handles potential NumPy array input due to testing harness errors.
"""

def transform(input_sequence: list[int]) -> list[int]:
    """
    Applies the transformation rule to the input sequence.

    Args:
        input_sequence: A list or NumPy array of integers (0s and 1s).

    Returns:
        A new list of integers where specific 0s are replaced by 3s based
        on neighboring 1s.
    """

    # Handle potential NumPy array input by converting to list if necessary
    if isinstance(input_sequence, np.ndarray):
        # Assuming a 1D array based on examples
        input_list = input_sequence.tolist()
    else:
        # Assume it's already a list or list-like
        input_list = list(input_sequence)

    # Initialize the output sequence as a copy of the input list
    output_sequence = list(input_list)
    n = len(input_list)

    # Iterate through each element of the input list by index
    for i in range(n):
        # Check if the current element is 0
        if input_list[i] == 0:
            # Initialize flags for neighbor conditions
            preceded_by_ones = False
            followed_by_ones = False

            # Check preceding neighbors: requires at least two elements before
            # current index i (i.e., indices i-2 and i-1 must be valid)
            if i >= 2:
                if input_list[i-2] == 1 and input_list[i-1] == 1:
                    preceded_by_ones = True

            # Check succeeding neighbors: requires at least two elements after
            # current index i (i.e., indices i+1 and i+2 must be valid)
            if i <= n - 3:
                if input_list[i+1] == 1 and input_list[i+2] == 1:
                    followed_by_ones = True

            # If the element is 0 and either neighbor condition is met,
            # change the corresponding element in the output sequence to 3
            if preceded_by_ones or followed_by_ones:
                output_sequence[i] = 3
        # No else needed: if conditions aren't met, the value remains unchanged
        # from the initial copy.

    # Return the modified sequence as a standard Python list
    return output_sequence