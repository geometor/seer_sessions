"""
Transforms a sequence of digits by identifying singular non-zero elements in the
original input sequence and spreading their value into adjacent zeros in a copied
sequence. A non-zero element is considered 'singular' if its immediate neighbors
(if they exist within the sequence boundaries) have different values. The spreading
occurs outwards (left and right) from the position of the singular element,
replacing only those elements that were originally zero in the input sequence.
The spread stops in a given direction when it encounters either a non-zero element
(from the original input sequence) or the boundary of the sequence. Elements
that were not originally zero, or zeros that were not reached by spreading from a
singular element, remain unchanged in the output.
"""

import copy
import numpy as np # Import numpy as input might be numpy array

def is_singular(sequence, index, n):
    """
    Checks if the element at the given index in the sequence is a singular non-zero element.

    Args:
        sequence: The input list or 1D array of integers (original sequence).
        index: The index of the element to check.
        n: The length of the sequence.

    Returns:
        True if the element is non-zero and singular, False otherwise.
    """
    current_val = sequence[index]

    # Must be non-zero to be considered for spreading
    if current_val == 0:
        return False

    # Check left neighbor condition:
    # True if it's the first element (index 0) OR the element to the left is different.
    left_neighbor_different = (index == 0 or sequence[index - 1] != current_val)

    # Check right neighbor condition:
    # True if it's the last element (index n-1) OR the element to the right is different.
    right_neighbor_different = (index == n - 1 or sequence[index + 1] != current_val)

    # Must satisfy both conditions to be singular
    return left_neighbor_different and right_neighbor_different

def transform(input_sequence):
    """
    Applies the spreading transformation rule to the input sequence.

    Args:
        input_sequence: A list or 1D numpy array of integers representing the input sequence.

    Returns:
        A list of integers representing the transformed output sequence.
    """

    # Ensure input is consistently a standard Python list for processing.
    # This guards against potential numpy-specific behavior or errors.
    if isinstance(input_sequence, np.ndarray):
        original_list = input_sequence.tolist() # Convert numpy array to list
    else:
        # Assume it's already list-like (e.g., list, tuple) and ensure it's a mutable list
        original_list = list(input_sequence)

    # Create a deep copy of the list. This copy will be modified and returned.
    # The original_list remains unchanged and is used for reference checks.
    output_list = copy.deepcopy(original_list)
    n = len(original_list)

    # Iterate through each index of the original sequence
    for i in range(n):
        # Check if the element at the current index 'i' in the original_list is singular
        if is_singular(original_list, i, n):
            # If it's singular, get its value for spreading
            spread_value = original_list[i]

            # --- Spread the value to the Left ---
            # Start checking from the element immediately to the left of the singular element
            j = i - 1
            # Continue spreading left as long as:
            # 1. The index 'j' is within the sequence bounds (j >= 0)
            # 2. The element at index 'j' in the *original* sequence was 0
            while j >= 0 and original_list[j] == 0:
                # Update the corresponding element in the output_list
                output_list[j] = spread_value
                # Move the index one step further left
                j -= 1

            # --- Spread the value to the Right ---
            # Start checking from the element immediately to the right of the singular element
            k = i + 1
            # Continue spreading right as long as:
            # 1. The index 'k' is within the sequence bounds (k < n)
            # 2. The element at index 'k' in the *original* sequence was 0
            while k < n and original_list[k] == 0:
                # Update the corresponding element in the output_list
                output_list[k] = spread_value
                # Move the index one step further right
                k += 1

    # After checking all elements and performing necessary spreading, return the modified list
    return output_list