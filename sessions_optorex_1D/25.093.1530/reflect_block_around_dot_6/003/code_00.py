"""
Transforms a 1D NumPy array of 12 integers based on the position of the number 2.
The number 2 acts as a pivot. Non-zero elements before the 2 are moved to
the slots *after* the 2 in the output, preserving their relative order and 
aligning them to the right end of the array.
Non-zero elements after the 2 are moved to the slots *before* the 2
in the output, preserving their relative order and aligning them to the right
(i.e., immediately before the pivot). The position of 2 remains unchanged.
All other positions are filled with 0.
"""

import numpy as np

def find_pivot_index(sequence, pivot_value=2):
    """Finds the index of the first occurrence of the pivot value in the sequence."""
    indices = np.where(sequence == pivot_value)[0]
    if len(indices) > 0:
        return indices[0]
    else:
        # Handle cases where the pivot might be missing, though based on examples it's always present.
        # Returning -1 or raising an error could be options. Let's return -1 for now.
        return -1

def extract_non_zero_elements(sub_sequence):
    """Extracts non-zero elements from a sub-sequence (NumPy array), preserving order."""
    return sub_sequence[sub_sequence != 0]

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the pivot-based sequence transformation to a NumPy array.

    Args:
        input_grid: A 1D NumPy array of 12 integers.

    Returns:
        A 1D NumPy array of 12 integers representing the transformed sequence.
    """
    # Define constants
    sequence_length = 12
    padding_value = 0
    pivot_value = 2

    # 1. Locate the index (position) of the pivot integer `2`.
    pivot_index = find_pivot_index(input_grid, pivot_value)

    # Basic error check if pivot is not found (unlikely based on examples)
    if pivot_index == -1:
        print(f"Warning: Pivot element {pivot_value} not found. Returning original grid.")
        return input_grid # Or handle as an error appropriately

    # 2. Extract non-zero elements before the pivot.
    elements_before = extract_non_zero_elements(input_grid[:pivot_index])

    # 3. Extract non-zero elements after the pivot.
    elements_after = extract_non_zero_elements(input_grid[pivot_index + 1:])

    # 4. Initialize the output sequence with padding values.
    output_grid = np.full(sequence_length, padding_value, dtype=input_grid.dtype)

    # 5. Place the pivot integer `2` into the output sequence at its original index.
    output_grid[pivot_index] = pivot_value

    # 6. Place the `elements_after` into the output sequence, ending just before the pivot index (right-aligned in the 'before' section).
    len_after = len(elements_after)
    if len_after > 0:
        start_index_after = pivot_index - len_after
        # Ensure start index is not negative (handles cases where there are more 'after' elements than space before pivot)
        if start_index_after >= 0:
            output_grid[start_index_after:pivot_index] = elements_after
        else:
             # This case suggests an issue if it occurs based on problem constraints
             print(f"Warning: Not enough space to place 'after' elements for pivot at {pivot_index}.")
             # Place as many as possible
             output_grid[0:pivot_index] = elements_after[-pivot_index:]


    # 7. Place the `elements_before` into the output sequence, starting after the pivot index and ending at the end of the array (right-aligned in the 'after' section).
    len_before = len(elements_before)
    if len_before > 0:
        start_index_before = sequence_length - len_before
        # Ensure start index is valid (it should be >= pivot_index + 1 if placement is possible)
        if start_index_before > pivot_index:
             output_grid[start_index_before:sequence_length] = elements_before
        else:
            # This case suggests an issue if it occurs based on problem constraints
            print(f"Warning: Not enough space to place 'before' elements for pivot at {pivot_index}.")
            # Place as many as possible starting right after pivot
            placeable_len = sequence_length - (pivot_index + 1)
            output_grid[pivot_index + 1 : sequence_length] = elements_before[:placeable_len]


    # 8. Return the resulting sequence.
    return output_grid