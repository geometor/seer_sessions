import math
import numpy as np # Although not strictly needed for list manipulation, good practice to import common libraries

"""
Identifies "single" non-zero digits in a sequence and propagates their value into adjacent blocks of zeros.
A non-zero digit is considered "single" if its immediate left and right neighbors (if they exist within the sequence bounds) have different values from it. In other words, it's a non-zero digit that is not part of a contiguous block of the same non-zero digit.
The value of each identified single digit replaces the zeros in the contiguous block(s) of zeros immediately to its left and/or right. Propagation stops when a non-zero digit or the boundary of the sequence is encountered.
"""

def is_single(input_list, index):
    """
    Checks if the digit at the given index in the input list is a 'single' non-zero digit.

    A digit is 'single' if it's non-zero and its immediate neighbors (if they exist)
    have different values.

    Args:
        input_list: The list of integers representing the sequence.
        index: The index of the digit to check.

    Returns:
        True if the digit at the index is single, False otherwise.
    """
    n = len(input_list)
    value = input_list[index]

    # Rule 1: Must be non-zero
    if value == 0:
        return False

    # Rule 2: Check left neighbor (if it exists) must be different
    left_different = (index == 0) or (input_list[index - 1] != value)

    # Rule 3: Check right neighbor (if it exists) must be different
    right_different = (index == n - 1) or (input_list[index + 1] != value)

    # Satisfies all rules if non-zero and different from existing neighbors
    return left_different and right_different

def transform(input_str: str) -> str:
    """
    Transforms an input sequence string based on the single digit propagation rule.

    It finds non-zero digits not part of a block of identical digits and propagates
    their value into adjacent zero blocks.

    Args:
        input_str: A string of space-separated digits (e.g., "0 0 4 1 1 0").

    Returns:
        A string of space-separated digits representing the transformed sequence.
    """
    # Parse input string into a list of integers
    input_list = [int(d) for d in input_str.split()]
    n = len(input_list)

    # Initialize output_list as a copy of the input list.
    # Modifications will be made to this list.
    output_list = list(input_list)

    # --- Identify single non-zero digits ---
    # Iterate through the original input list to find digits that meet the 'single' criteria.
    singles = []
    for i in range(n):
        if is_single(input_list, i):
            # Store the index and value of each single digit found.
            singles.append({"index": i, "value": input_list[i]})

    # --- Propagate values into adjacent zeros ---
    # Iterate through the identified single digits.
    for single in singles:
        idx = single["index"]
        val = single["value"]

        # Propagate to the left:
        # Start from the position immediately left of the single digit.
        j = idx - 1
        # Move leftwards as long as we are within bounds and encounter zeros in the *original* input.
        # Checking the original input prevents propagation into areas filled by other singles in this step.
        while j >= 0 and input_list[j] == 0:
            # Update the corresponding position in the output list with the single digit's value.
            output_list[j] = val
            j -= 1 # Move one step further left.

        # Propagate to the right:
        # Start from the position immediately right of the single digit.
        j = idx + 1
        # Move rightwards as long as we are within bounds and encounter zeros in the *original* input.
        while j < n and input_list[j] == 0:
            # Update the corresponding position in the output list with the single digit's value.
            output_list[j] = val
            j += 1 # Move one step further right.

    # Format the final output list back into a space-separated string.
    output_str = " ".join(map(str, output_list))
    return output_str