"""
Transforms an input sequence of 12 integers by identifying the first
contiguous block of non-zero integers and shifting this block 4 positions
to the right within a new sequence initialized with zeros. If the shifted
block extends beyond the sequence boundaries, only the portion that fits
is placed.
"""

import numpy as np

def find_first_non_zero_block(grid: np.ndarray) -> tuple[int, np.ndarray | None]:
    """
    Finds the first contiguous block of non-zero integers in a NumPy array.

    Args:
        grid: A 1D NumPy array of integers.

    Returns:
        A tuple containing:
        - start_index: The starting index of the block (or -1 if not found).
        - payload: A NumPy array containing the non-zero integers in the block
                   (or None if not found). Returns only the *first* block if
                   multiple disjoint blocks exist.
    """
    # Find indices of all non-zero elements
    non_zero_indices = np.where(grid != 0)[0]

    # Handle case with no non-zero elements
    if non_zero_indices.size == 0:
        return -1, None

    # The start index is the first non-zero index found
    start_index = non_zero_indices[0]

    # Determine the end index of the first contiguous block
    if non_zero_indices.size == 1:
        # Only one non-zero element, block length is 1
        end_index = start_index
    else:
        # Check for gaps between non-zero indices
        diffs = np.diff(non_zero_indices)
        # Find the index *within diffs* where the first gap (> 1) occurs
        gaps = np.where(diffs > 1)[0]
        if gaps.size == 0:
            # No gaps, the block extends to the last non-zero element found
            end_index = non_zero_indices[-1]
        else:
            # Gaps exist, the first block ends at the index just before the first gap
            # gaps[0] is the index in `diffs` where the first difference > 1 occurs.
            # This corresponds to the index in `non_zero_indices` *before* the gap.
            end_index = non_zero_indices[gaps[0]]

    # Extract the payload (the actual non-zero numbers in the identified block)
    # Slicing is [start:end+1] to include the element at end_index
    payload = grid[start_index : end_index + 1]

    return start_index, payload


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input NumPy array.
    """
    # Get the size of the input grid (expected to be 12)
    n = input_grid.shape[0]

    # 1. Initialize a new output sequence of length n with all zeros.
    output_grid = np.zeros_like(input_grid)

    # 2. Find the start index and the payload (first non-zero block)
    start_index, payload = find_first_non_zero_block(input_grid)

    # 3. Proceed only if a non-zero block was found
    if start_index != -1 and payload is not None:
        # 4. Calculate the target start index for the shift (shift right by 4)
        target_start_index = start_index + 4
        payload_len = payload.shape[0]

        # 5. Calculate the theoretical target end index (exclusive) for slicing
        target_end_index = target_start_index + payload_len

        # 6. Determine the actual slice boundaries within the output grid [0, n)
        # The slice in the output grid cannot start before index 0 or at/after index n.
        actual_output_start = max(0, target_start_index)
        actual_output_start = min(actual_output_start, n) # Clamp start to be at most n (effectively making slice empty if target_start_index >= n)

        # The slice in the output grid cannot end after index n.
        actual_output_end = min(n, target_end_index)
        # Ensure the end index is not smaller than the start index (can happen if clamped)
        actual_output_end = max(actual_output_start, actual_output_end)

        # 7. Determine the portion of the payload to copy based on calculated boundaries
        # If the target start was negative, we need to skip elements from the beginning of the payload.
        payload_start_offset = max(0, -target_start_index)
        # The number of elements we can actually copy is the length of the valid slice in the output grid.
        payload_copy_len = actual_output_end - actual_output_start

        # 8. Copy the relevant part of the payload if there's space and content to copy
        # Check if there's a valid length to copy and if the offset doesn't exceed the payload length
        if payload_copy_len > 0 and payload_start_offset < payload_len:
            # Select the correct sub-slice of the payload to copy
            payload_to_copy = payload[payload_start_offset : payload_start_offset + payload_copy_len]
            # Assign the selected payload slice to the calculated output slice
            output_grid[actual_output_start:actual_output_end] = payload_to_copy

    # 9. Return the transformed grid
    return output_grid