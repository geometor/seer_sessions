import numpy as np
from typing import List, Tuple, Optional

"""
Transforms an input sequence of integers based on the following rules:
1.  Locate the index of the fixed pivot element '2'.
2.  Identify the *first* contiguous block of identical non-zero numbers (excluding the pivot), known as the 'payload'.
3.  Create an output sequence of the same length, initialized with zeros.
4.  Place the pivot '2' in the output sequence at its original index.
5.  Determine the payload's new location based on its original position relative to the pivot:
    a.  If the payload was originally *before* the pivot, count the zeros strictly between the payload's end and the pivot's start in the input. The payload is moved to the output starting at index: pivot_index + 1 + count_of_intermediate_zeros.
    b.  If the payload was originally *after* the pivot, it is moved to the beginning of the output sequence (index 0).
6.  Return the output sequence with the pivot and relocated payload, with remaining positions as zeros.
"""

# --- Helper Functions ---

def find_pivot_np(grid: np.ndarray) -> Optional[int]:
    """Finds the index of the pivot element (2) in a NumPy array."""
    indices = np.where(grid == 2)[0]
    # Return the index if found, otherwise None
    return indices[0] if len(indices) > 0 else None

def find_payload_np(grid: np.ndarray, pivot_index: Optional[int]) -> Optional[Tuple[int, int, int]]:
    """
    Finds the first contiguous payload block (value, start_index, end_index_inclusive)
    in a NumPy array, excluding the pivot.
    Returns None if no suitable payload is found.
    """
    payload_value = None
    payload_start_index = -1
    payload_end_index = -1 # Will store the end index of the identified block

    # Get indices of all non-zero elements
    indices_non_zero = np.where(grid != 0)[0]

    # Filter out the pivot index itself if it exists
    if pivot_index is not None:
        indices_non_zero = indices_non_zero[indices_non_zero != pivot_index]

    # If no non-zero elements (besides potentially the pivot) exist, return None
    if len(indices_non_zero) == 0:
        return None

    # Iterate through the non-zero indices to find the first contiguous block
    current_val = -1
    current_start = -1
    current_end = -1
    found_block = None # To store the first completed block

    for i, idx in enumerate(indices_non_zero):
        val = grid[idx]

        if current_start == -1: # Starting a potential new block
            current_val = val
            current_start = idx
            current_end = idx
        elif val == current_val and idx == current_end + 1: # Continuing the current block
            current_end = idx
        else: # The previous block ended, or this element starts a different block
            # Since we only care about the *first* block, we can store it and stop
            payload_value = grid[current_start]
            payload_start_index = current_start
            payload_end_index = current_end # End index of the first block
            found_block = (payload_value, payload_start_index, payload_end_index)
            break # Exit the loop once the first block is fully identified

    # Check if the loop finished without breaking (means the first/only block extended to the end)
    if found_block is None and current_start != -1:
        payload_value = grid[current_start]
        payload_start_index = current_start
        payload_end_index = current_end # The end index was updated correctly
        found_block = (payload_value, payload_start_index, payload_end_index)

    return found_block


def count_intermediate_zeros_np(grid: np.ndarray, payload_end_index: int, pivot_index: int) -> int:
    """Counts zeros strictly between the end of the payload and the pivot in a NumPy array."""
    count = 0
    # Ensure indices allow for intermediate elements and payload is indeed before pivot
    if payload_end_index >= 0 and pivot_index >=0 and payload_end_index < pivot_index - 1:
        # Extract the slice between the payload end and pivot start
        intermediate_slice = grid[payload_end_index + 1 : pivot_index]
        # Count the number of zeros in this slice
        count = np.count_nonzero(intermediate_slice == 0)
    return count

# --- Main Transformation Function ---

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input grid (NumPy array).
    """
    # Get the size of the input grid
    n = len(input_grid)
    # Initialize output_grid with zeros of the same size
    output_grid = np.zeros(n, dtype=input_grid.dtype)

    # 1. Locate the pivot index
    pivot_index = find_pivot_np(input_grid)
    if pivot_index is None:
        # If no pivot '2' is found, return the zero grid (or handle as error)
        # Based on problem description, pivot should always exist.
        print("Warning: Pivot '2' not found in input.")
        return output_grid # Return zero grid as a fallback

    # 2. Place the pivot '2' in the output grid at its original index
    output_grid[pivot_index] = 2

    # 3. Identify the payload block (value, start index, end index)
    payload_info = find_payload_np(input_grid, pivot_index)
    if payload_info is None:
        # If no payload found (other than pivot), return the grid with only the pivot placed
        # Based on problem description, a payload should always exist.
        print("Warning: Payload not found in input.")
        return output_grid # Return grid with only pivot

    # Extract payload details
    payload_value, payload_start_index, payload_end_index = payload_info
    payload_len = payload_end_index - payload_start_index + 1
    # Create the payload block as a NumPy array
    payload_block = np.full(payload_len, payload_value, dtype=input_grid.dtype)

    # 4. Determine payload placement based on its position relative to the pivot
    if payload_start_index < pivot_index:
        # Case A: Payload was *before* the pivot

        # a. Count intermediate zeros between payload end and pivot start
        intermediate_zeros = count_intermediate_zeros_np(input_grid, payload_end_index, pivot_index)

        # b. Calculate the target start index in the output grid
        target_start_index = pivot_index + 1 + intermediate_zeros

        # c. Place the payload block in the output grid, ensuring it fits within bounds
        target_end_index_exclusive = target_start_index + payload_len
        if target_end_index_exclusive <= n:
            # Fits completely
            output_grid[target_start_index : target_end_index_exclusive] = payload_block
        else:
            # Payload overflows the grid boundary, place only the part that fits
            fit_len = n - target_start_index
            if fit_len > 0:
                output_grid[target_start_index : n] = payload_block[:fit_len]
            # Consider logging a warning if overflow happens, as it might indicate unexpected input/logic issues

    else: # payload_start_index > pivot_index
        # Case B: Payload was *after* the pivot

        # a. Place the payload block at the beginning (index 0) of the output grid
        target_end_index_exclusive = payload_len
        if target_end_index_exclusive <= n:
            # Fits completely
            output_grid[0 : target_end_index_exclusive] = payload_block
        else:
            # Payload is longer than the grid, place only the part that fits
            output_grid[0 : n] = payload_block[:n]
            # Consider logging a warning if overflow happens

    # 5. Return the fully constructed output grid
    return output_grid