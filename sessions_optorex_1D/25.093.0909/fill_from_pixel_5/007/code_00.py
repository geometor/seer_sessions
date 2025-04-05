import numpy as np
import math # Although not used in the final version, imported as per template requirement

"""
Identifies "single" non-zero digits in an input sequence (list or array of 12 integers) 
and propagates their value into adjacent blocks of zeros based on the original input state.

A non-zero digit is considered "single" if its immediate left and right neighbors 
(if they exist within the sequence bounds) have different values from it in the 
original input sequence. It's essentially a non-zero digit not part of a 
contiguous block of the same non-zero digit.

The value of each identified single digit (based on the original input) replaces 
the zeros in the contiguous block(s) of zeros immediately to its left and/or 
right in an output sequence. Propagation stops when a non-zero digit (in the 
original input) or the boundary of the sequence is encountered.
"""

def _is_single(sequence, index):
    """
    Helper function to check if the digit at the given index is a 'single' non-zero digit.

    Args:
        sequence: The list of integers representing the sequence.
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
    Applies the single digit propagation rule to the input sequence.

    Args:
        input_sequence: A list, NumPy array, or similar iterable of 12 integers.

    Returns:
        A list of 12 integers representing the transformed sequence.
    """
    
    # --- Input Handling & Initialization ---
    # Ensure input is a standard Python list of integers for consistent processing
    if isinstance(input_sequence, np.ndarray):
         input_list = input_sequence.astype(int).tolist() # Convert numpy array to list
    else:
         # Handles lists, tuples, strings of space-separated numbers etc.
         try:
             if isinstance(input_sequence, str):
                 input_list = [int(d) for d in input_sequence.split()]
             else:
                 input_list = list(map(int, input_sequence)) # Assume iterable, convert elements to int
         except (ValueError, TypeError):
             raise TypeError("Input must be convertible to a list of integers.")

    n = len(input_list)
    # Optional: Could add check here if n != 12 and raise error or warning

    # Initialize output_sequence as a mutable copy of the processed input list.
    # Modifications will be made to this list.
    output_sequence = list(input_list)

    # --- Step 1: Identify all single non-zero digits in the ORIGINAL input list ---
    singles = []
    # Iterate through each index of the input list
    for i in range(n):
        # Use the helper function to check if the element at index 'i' is single
        if _is_single(input_list, i):
            # Store the index and value of each single digit found.
            singles.append({"index": i, "value": input_list[i]})

    # --- Step 2: Propagate values from identified singles into adjacent zeros ---
    # Iterate through the list of single digits identified in Step 1.
    for single in singles:
        idx = single["index"] # Original index of the single digit
        val = single["value"] # Value of the single digit

        # --- Propagate to the left ---
        # Start checking from the position immediately left of the single digit.
        j = idx - 1
        # Keep moving left as long as we are within the sequence bounds (j >= 0)
        # AND the element at position 'j' in the ORIGINAL input_list is 0.
        # This prevents propagation over non-zeros or into areas potentially filled by other singles
        # if we were checking the output_sequence directly during propagation.
        while j >= 0 and input_list[j] == 0:
            # Update the corresponding position in the output_sequence with the single digit's value.
            output_sequence[j] = val
            j -= 1 # Move one step further left.

        # --- Propagate to the right ---
        # Start checking from the position immediately right of the single digit.
        j = idx + 1
        # Keep moving right as long as we are within the sequence bounds (j < n)
        # AND the element at position 'j' in the ORIGINAL input_list is 0.
        while j < n and input_list[j] == 0:
            # Update the corresponding position in the output_sequence with the single digit's value.
            output_sequence[j] = val
            j += 1 # Move one step further right.

    # Return the modified output sequence as a list.
    return output_sequence