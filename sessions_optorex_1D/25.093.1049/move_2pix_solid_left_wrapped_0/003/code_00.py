import numpy as np
import collections # Although not strictly needed in the final version, it was considered during analysis

"""
Transforms an input list/array of 12 digits by shifting the positions of all '0' elements 
two steps to the left (with wrap-around, modulo 12) and filling the remaining positions 
with the non-zero elements from the input list, preserving their original relative order.
"""

def transform(input_list):
    """
    Applies the described transformation to the input list or NumPy array.

    Args:
        input_list: A list or 1D NumPy array of 12 integers.

    Returns:
        A list of 12 integers representing the transformed list.
    """
    # Ensure input is treated as a list for consistent indexing and operations
    # The previous error showed input can be a numpy array.
    if isinstance(input_list, np.ndarray):
        # Assuming a 1D array based on examples. If it could be multi-dimensional,
        # flattening or specific axis selection might be needed.
        input_list = input_list.tolist()

    list_length = 12
    if len(input_list) != list_length:
        # Basic validation, though problem context implies fixed length
        raise ValueError(f"Input list must have length {list_length}")

    # Initialize the output list with a placeholder value (None).
    # This makes it easy to identify slots not filled by the shifted zeros.
    output_list = [None] * list_length

    # --- Step 1: Collect non-zero elements and calculate target indices for zeros ---
    non_zero_elements = []
    zero_source_indices = [] # Keep track of original zero positions

    for i, element in enumerate(input_list):
        if element == 0:
            zero_source_indices.append(i)
        else:
            non_zero_elements.append(element) # Collect non-zeros in order

    # Calculate the target indices for the zeros based on their source indices
    zero_target_indices = []
    for i in zero_source_indices:
        target_index = (i - 2) % list_length # Shift left by 2, wrap around
        zero_target_indices.append(target_index)

    # --- Step 2: Place the zeros in their calculated target positions ---
    # It's possible multiple zeros map to the same target if the original zeros
    # were exactly list_length apart, but the logic focuses on *where* zeros land.
    for index in zero_target_indices:
        output_list[index] = 0

    # --- Step 3: Fill the remaining placeholder positions with non-zero elements ---
    non_zero_iter = iter(non_zero_elements) # Use an iterator for efficient sequential access

    for i in range(list_length):
        if output_list[i] is None: # Check if the slot is empty (not filled by a zero)
            try:
                # Fill with the next available non-zero element
                output_list[i] = next(non_zero_iter)
            except StopIteration:
                # This condition implies a mismatch between the number of zero target slots
                # and the number of non-zero elements collected, which shouldn't happen
                # if the input always has 12 elements.
                print(f"Error: Inconsistent state - ran out of non-zero elements. Input: {input_list}")
                # Decide on error handling: break, raise exception, or fill with default?
                # For robustness, perhaps fill remaining Nones with 0 or raise error.
                # For now, just print error and potentially leave Nones.
                break # Exit the loop if error occurs


    # Final check for placeholders (optional, for debugging)
    if None in output_list:
         print(f"Warning: Output list still contains placeholders. Input: {input_list}, Partially Filled Output: {output_list}")
         # Replace None with a default if required by the task specification
         # output_list = [val if val is not None else 0 for val in output_list]


    # Return the transformed list. The problem description doesn't explicitly state
    # the required output type (list vs numpy array). Returning list is safer based on Python implementation.
    return output_list