"""
Transforms an input sequence of integers (0s and 1s) based on a local rule.
The rule identifies sequences of exactly two consecutive '1's ([1, 1]).
When such a sequence is found at index i and i+1 in the input sequence:
1. If an element exists before the sequence (at index i-1) and its value is 0,
   that element's value in the output sequence is changed to 3.
2. If an element exists after the sequence (at index i+2) and its value is 0,
   that element's value in the output sequence is changed to 3.
All other elements from the input sequence remain unchanged in the output sequence.
Modifications are based on the original input state and applied to a separate output sequence.
"""

import math # Although not used in this specific logic, good practice to import common libraries if potentially needed
import copy  # Used for creating a mutable copy of the input

def transform(input_sequence):
    """
    Applies the transformation rule to the input sequence.

    Args:
        input_sequence: A list of integers (0s and 1s).

    Returns:
        A new list of integers representing the transformed sequence (0s, 1s, and 3s).
    """
    # Initialize output_sequence as a copy of the input_sequence
    # This ensures modifications don't affect subsequent checks based on the original input
    output_sequence = copy.deepcopy(input_sequence)
    n = len(input_sequence)

    # Iterate through the input sequence to find the [1, 1] pattern
    # We only need to check up to the second-to-last element (n-2)
    # because we are looking at pairs input_sequence[i] and input_sequence[i+1]
    for i in range(n - 1):
        # Check if the current element and the next element form the [1, 1] pattern
        if input_sequence[i] == 1 and input_sequence[i+1] == 1:
            # If the pattern is found, check neighbors in the original input_sequence

            # Check the element *before* the pattern (at index i-1)
            # Ensure the index i-1 is valid (i > 0)
            if i > 0:
                # Check if the preceding element in the original sequence is 0
                if input_sequence[i-1] == 0:
                    # If it is 0, change the corresponding element in the output_sequence to 3
                    output_sequence[i-1] = 3

            # Check the element *after* the pattern (at index i+2)
            # Ensure the index i+2 is valid (i+2 < n)
            if i + 2 < n:
                # Check if the succeeding element in the original sequence is 0
                if input_sequence[i+2] == 0:
                    # If it is 0, change the corresponding element in the output_sequence to 3
                    output_sequence[i+2] = 3

    # Return the modified sequence
    return output_sequence
