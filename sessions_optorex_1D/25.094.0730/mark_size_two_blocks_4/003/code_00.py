import numpy as np
from typing import List

"""
Transforms a sequence of 0s and 1s by identifying the pattern [0, 1, 1, 0]. 
For each occurrence of this pattern found in the input sequence starting at index i, 
the elements at index i (the first 0) and index i+3 (the second 0) are replaced 
with 3 in the output sequence. All other elements, including the 1s within the 
pattern, remain unchanged. Modifications are based on the original input to 
prevent cascading effects within a single transformation pass.
"""

def transform(input_sequence: List[int]) -> List[int]:
    """
    Applies the [0, 1, 1, 0] -> [3, 1, 1, 3] transformation rule.

    Args:
        input_sequence: A list of integers (0s and 1s).

    Returns:
        A new list of integers representing the transformed sequence.
    """
    n = len(input_sequence)
    # Initialize the output sequence as a copy of the input sequence.
    # Changes will be made to this copy based on patterns found in the input.
    output_sequence = list(input_sequence) 

    # Define the target pattern
    pattern = [0, 1, 1, 0]
    pattern_len = len(pattern)

    # Iterate through the input sequence to find occurrences of the pattern.
    # The loop stops early enough to allow a full pattern check.
    for i in range(n - pattern_len + 1):
        # Check if the slice of the input sequence matches the target pattern.
        if input_sequence[i:i+pattern_len] == pattern:
            # If the pattern matches, modify the corresponding elements
            # in the output sequence.
            # Change the element at the start of the pattern match (index i)
            output_sequence[i] = 3
            # Change the element at the end of the pattern match (index i + 3)
            output_sequence[i + pattern_len - 1] = 3 # i + 3 in this case

    # Return the modified output sequence.
    return output_sequence
