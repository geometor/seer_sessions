import math
import numpy as np # Common library, though not strictly needed for this logic

"""
Identifies "single" non-zero digits in an input sequence (list or NumPy array of 12 integers) and propagates their value into adjacent blocks of zeros.
A non-zero digit is considered "single" if its immediate left and right neighbors (if they exist within the sequence bounds) have different values from it.
The value of each identified single digit (based on the original input) replaces the zeros in the contiguous block(s) of zeros immediately to its left and/or right in an output sequence. Propagation stops when a non-zero digit (in the original input) or the boundary of the sequence is encountered.
"""

def is_single(sequence, index):
    """
    Checks if the digit at the given index in the sequence is a 'single' non-zero digit.

    A digit is 'single' if it's non-zero and its immediate neighbors (if they exist)
    have different values.

    Args:
        sequence: The list or array of integers representing the sequence.
        index: The index of the digit to check.

    Returns:
        True if the digit at the index is single, False otherwise.
    """
    n = len(sequence)
    value = sequence[index]

    # Rule 1: Must be non-zero
    if value == 0:
        return False

    # Rule 2: Check left neighbor (if it exists) must be different
    # True if it's the first element OR the element to the left is different
    left_different = (index == 0) or (sequence[index - 1] != value)

    # Rule 3: Check right neighbor (if it exists) must be different
    # True if it's the last element OR the element to the right is different
    right_different = (index == n - 1) or (sequence[index + 1] != value)

    # Satisfies all rules if non-zero and different from existing neighbors
    return left_different and right_different

def transform(input_sequence):
    """
    Transforms an input sequence based on the single digit propagation rule.

    Args:
        input_sequence: A list or NumPy array of 12 integers.

    Returns:
        A list of 12 integers representing the transformed sequence.
    """
    n = len(input_sequence)
    # Initialize output_sequence as a mutable copy (list) of the input sequence.
    # We will modify this copy.
    output_sequence = list(input_sequence)

    # --- Step 1: Identify all single non-zero digits in the ORIGINAL input sequence ---
    singles = []
    for i in range(n):
        # Use the helper function to check if the element at index 'i' is single
        if is_single(input_sequence, i):
            # Store the index and value of each single digit found.
            singles.append({"index": i, "value": input_sequence[i]})

    # --- Step 2: Propagate values from identified singles into adjacent zeros ---
    # Iterate through the list of single digits identified in Step 1.
    for single in singles:
        idx = single["index"] # Original index of the single digit
        val = single["value"] # Value of the single digit

        # --- Propagate to the left ---
        # Start checking from the position immediately left of the single digit.
        j = idx - 1
        # Keep moving left as long as we are within the sequence bounds (j >= 0)
        # AND the element at position 'j' in the ORIGINAL input_sequence is 0.
        while j >= 0 and input_sequence[j] == 0:
            # Update the corresponding position in the output_sequence with the single digit's value.
            output_sequence[j] = val
            j -= 1 # Move one step further left.

        # --- Propagate to the right ---
        # Start checking from the position immediately right of the single digit.
        j = idx + 1
        # Keep moving right as long as we are within the sequence bounds (j < n)
        # AND the element at position 'j' in the ORIGINAL input_sequence is 0.
        while j < n and input_sequence[j] == 0:
            # Update the corresponding position in the output_sequence with the single digit's value.
            output_sequence[j] = val
            j += 1 # Move one step further right.

    # Return the modified output sequence.
    return output_sequence