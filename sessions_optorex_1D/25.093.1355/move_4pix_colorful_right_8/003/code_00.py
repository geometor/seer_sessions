import numpy as np
import math # Although math might not be needed here, it's available.

"""
Transforms an input array (list or numpy array) of 12 digits by identifying the segment between the first and last non-zero digits (inclusive) and shifting this segment 4 positions to the right. The output array is initialized with zeros, and the shifted segment overwrites the zeros at the target positions. Elements shifted beyond the 12th position are truncated. If the input array contains only zeros, it is returned unchanged.
"""

def _find_non_zero_indices(int_list: list[int] | np.ndarray) -> tuple[int | None, int | None]:
    """
    Finds the index of the first and last non-zero elements in a list or NumPy array.
    Returns (None, None) if no non-zero elements are found.
    """
    # Convert potential NumPy array to list for easier iteration/index finding,
    # or directly use NumPy functions if preferred.
    if isinstance(int_list, np.ndarray):
        # Find indices of non-zero elements using NumPy
        non_zero_indices = np.nonzero(int_list)[0]
        if non_zero_indices.size == 0:
            return None, None
        else:
            return non_zero_indices[0], non_zero_indices[-1]
    else: # Assume it's a list
        first_nz = -1
        last_nz = -1
        for i, digit in enumerate(int_list):
            if digit != 0:
                if first_nz == -1:
                    first_nz = i
                last_nz = i
        if first_nz == -1:
            return None, None
        return first_nz, last_nz

def transform(input_array: list[int] | np.ndarray) -> list[int] | np.ndarray:
    """
    Applies the segment shift transformation rule to the input array.

    Workflow:
    1. Determine the length of the input array (assumed to be 12 based on examples).
    2. Identify the first and last non-zero element indices ('first_nz', 'last_nz') using a helper function.
    3. If all elements are zero (first_nz is None), return a copy of the original input array.
    4. Extract the segment of the input array from first_nz to last_nz (inclusive).
    5. Initialize an output array of the same length with all zeros. Ensure the output type matches the input type if possible (e.g., NumPy array if input is NumPy array).
    6. Calculate the target start index for placing the segment in the output array (first_nz + 4).
    7. Iterate through the extracted segment. For each element and its index 'i' within the segment:
       a. Calculate the corresponding target index in the output array: target_start_index + i.
       b. If the target index is within the bounds of the output array (0 to length-1), place the element at that index.
       c. Otherwise (if target index >= length), the element is shifted out of bounds and ignored (truncated).
    8. Return the resulting output array.
    """
    # Step 1: Get length and handle input type
    list_length = len(input_array)
    is_numpy = isinstance(input_array, np.ndarray)

    # Step 2: Identify the first and last non-zero element indices
    first_nz, last_nz = _find_non_zero_indices(input_array)

    # Step 3: Handle the all-zeros case
    if first_nz is None:
        # Return a copy to avoid modifying the original input if it's mutable
        return np.copy(input_array) if is_numpy else list(input_array)

    # Step 4: Extract the non-zero segment
    segment = input_array[first_nz : last_nz + 1]

    # Step 5: Initialize the output array with zeros
    # Match output type to input type
    if is_numpy:
        # Ensure the dtype matches the input array's dtype
        output_array = np.zeros(list_length, dtype=input_array.dtype)
    else:
        output_array = [0] * list_length

    # Step 6: Calculate the target start position for the shift
    shift_amount = 4
    target_start_index = first_nz + shift_amount

    # Step 7: Place the segment into the output array at the shifted position
    for i, digit in enumerate(segment):
        target_index = target_start_index + i
        # Check bounds: Only place if the target index is within the list length
        if 0 <= target_index < list_length:
            output_array[target_index] = digit
        # Elements shifted beyond the end are implicitly truncated

    # Step 8: Return the resulting output array
    return output_array