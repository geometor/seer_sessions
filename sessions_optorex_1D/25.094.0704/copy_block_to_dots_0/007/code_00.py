import copy
import math  # Available, but not needed for this rule
import numpy as np # Available, but standard lists are sufficient

"""
Transforms an input sequence of integers by identifying isolated non-zero digits 'N' 
(pattern '0 N 0', where N > 0) in the original sequence and replacing the triplet 
with 'N N N' in the output sequence. Elements not part of such a pattern are copied directly.
The transformation checks are based solely on the original input state.
"""

def transform(input_sequence: list[int]) -> list[int]:
    """
    Applies the transformation rule to the input sequence.

    Args:
        input_sequence: A list of integers representing the input sequence.

    Returns:
        A list of integers representing the transformed sequence.
    """
    # Get the length of the input sequence
    n = len(input_sequence)
    
    # Initialize the output sequence as a direct copy of the input sequence.
    # Modifications will be made to this copy based on patterns found in the original input.
    # Using deepcopy ensures that if the input contained mutable objects (not the case here, but good practice), they would also be copied.
    output_sequence = copy.deepcopy(input_sequence) 

    # Handle edge case: sequences shorter than 3 elements cannot contain the '0 N 0' pattern.
    if n < 3:
        return output_sequence # Return the unchanged copy

    # Iterate through the input sequence to find the '0 N 0' pattern.
    # The loop runs from the second element (index 1) up to the second-to-last element (index n-2),
    # as we need to check the element itself and its immediate neighbors (i-1, i, i+1).
    for i in range(1, n - 1):
        # Check the values at the current position and its neighbors in the *original* input sequence.
        # This is crucial: decisions are based only on the input state, not intermediate changes to output_sequence.
        prev_val = input_sequence[i - 1]
        curr_val = input_sequence[i] # This is the potential 'N'
        next_val = input_sequence[i + 1]

        # Check if the pattern '0 N 0' is met (where N is non-zero).
        if prev_val == 0 and curr_val != 0 and next_val == 0:
            # If the pattern is found, update the corresponding triplet in the output sequence.
            # The non-zero value N (curr_val) expands to replace the adjacent zeros in the output.
            output_sequence[i - 1] = curr_val
            # output_sequence[i] is already curr_val because we copied the input, 
            # but explicitly setting it reinforces the 'N N N' output pattern.
            output_sequence[i]     = curr_val 
            output_sequence[i + 1] = curr_val

    # Return the modified sequence.
    return output_sequence