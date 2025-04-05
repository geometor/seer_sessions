import numpy as np

"""
Transforms a sequence of digits based on the comparison of its first and last non-zero elements and the counts of leading/trailing zeros.

1. Find the first non-zero element (value F, index Fi) and the last non-zero element (value L, index Li).
2. If no non-zero elements exist, return the sequence unchanged.
3. Count leading zeros (LZ = Fi) and trailing zeros (TZ = length - 1 - Li).
4. Apply the following rules:
    a. If F > L: Fill the trailing zeros (indices > Li) with L.
    b. If F <= L:
        i. If LZ >= TZ: Fill the leading zeros (indices < Fi) with F.
        ii. If LZ < TZ: Fill the trailing zeros (indices > Li) with L.
"""

def find_first_non_zero(arr):
    """Finds the index and value of the first non-zero element in a numpy array."""
    non_zero_indices = np.where(arr != 0)[0]
    if len(non_zero_indices) == 0:
        return None, None  # No non-zero elements found
    first_nz_index = non_zero_indices[0]
    first_nz_value = arr[first_nz_index]
    return first_nz_index, first_nz_value

def find_last_non_zero(arr):
    """Finds the index and value of the last non-zero element in a numpy array."""
    non_zero_indices = np.where(arr != 0)[0]
    if len(non_zero_indices) == 0:
        return None, None  # No non-zero elements found
    last_nz_index = non_zero_indices[-1]
    last_nz_value = arr[last_nz_index]
    return last_nz_index, last_nz_value

def transform(input_arr):
    """
    Applies the transformation rule to the input numpy array.
    """
    # Ensure input is a numpy array (though context suggests it already is)
    if not isinstance(input_arr, np.ndarray):
        input_arr = np.array(input_arr)
        
    # Make a copy to modify
    output_arr = input_arr.copy()
    
    # Find boundaries
    first_nz_idx, first_nz_val = find_first_non_zero(input_arr)
    last_nz_idx, last_nz_val = find_last_non_zero(input_arr)

    # Handle edge case: all zeros or no non-zeros
    if first_nz_idx is None:
        return output_arr # Return the original array copy

    # Calculate zero counts
    leading_zeros = first_nz_idx
    trailing_zeros = len(input_arr) - 1 - last_nz_idx

    # Apply Hypothesis 16 logic
    if first_nz_val > last_nz_val:
        # Rule 1: Fill Trailing Zeros with Last Non-Zero Value
        if trailing_zeros > 0:
             output_arr[last_nz_idx + 1:] = last_nz_val
    else: # first_nz_val <= last_nz_val
        # Rule 2a: Leading Zeros >= Trailing Zeros -> Fill Leading with First Non-Zero Value
        if leading_zeros >= trailing_zeros:
            if leading_zeros > 0:
                output_arr[:first_nz_idx] = first_nz_val
        # Rule 2b: Leading Zeros < Trailing Zeros -> Fill Trailing with Last Non-Zero Value
        else: # leading_zeros < trailing_zeros
             if trailing_zeros > 0:
                output_arr[last_nz_idx + 1:] = last_nz_val

    return output_arr