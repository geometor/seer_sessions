```python
"""
Transforms an input sequence (1D NumPy array) of single-digit integers by swapping the relative position of a contiguous 'group' block (identical non-zero, non-2 digits) around a fixed 'pivot' element (2), while preserving the number of zeros ('gap') originally between them.

1. Find the index of the pivot element (2).
2. Find the contiguous block of the group element (X), its value, length, start index, and end index.
3. Keep the pivot element (2) at its original index in the output sequence.
4. Determine if the group block was positioned before or after the pivot in the input.
5. Calculate the gap size (number of zeros) strictly between the pivot and the group block in the input sequence.
6. Move the group block to the opposite side of the pivot in the output sequence, placing it such that the calculated gap size is maintained between the pivot and the nearest boundary of the group block.
7. Fill all other positions in the output sequence with zeros.
"""

import numpy as np

def _find_pivot_index(grid: np.ndarray) -> int:
    """Finds the index of the pivot element '2'."""
    pivot_indices = np.where(grid == 2)[0]
    if len(pivot_indices) == 1:
        return int(pivot_indices[0]) # Return as standard Python int
    else:
        # According to problem description, there should always be exactly one '2'
        raise ValueError("Input grid must contain exactly one pivot element '2'.")

def _find_group_info(grid: np.ndarray) -> tuple[int, int, int, int]:
    """
    Finds the contiguous block of identical non-zero digits (not '2').
    Returns:
        tuple: (group_value, start_index, end_index, length) or raises ValueError if not found.
    """
    group_value = None
    start_index = -1
    length = 0
    in_group = False
    found_group = False

    for i, val in enumerate(grid):
        # Check if the value is a potential group element
        if val != 0 and val != 2:
            if not in_group:
                # Start of a potential group
                group_value = int(val) # Store as standard Python int
                start_index = i
                length = 1
                in_group = True
            elif val == group_value:
                # Continue the current group
                length += 1
            else:
                # Found a different non-zero, non-2 digit.
                # Problem implies only one group type, so we stop the first one found.
                found_group = True
                break # Exit loop once the first complete group is identified
        elif in_group:
            # Group ended (hit a 0 or 2)
            found_group = True
            break # Exit loop once the group ends

    # Handle case where group runs to the end of the array
    if in_group and not found_group:
        found_group = True

    if found_group:
        end_index = start_index + length - 1
        # Return standard Python ints
        return group_value, int(start_index), int(end_index), int(length)
    else:
        # According to problem description, there should always be a group
        raise ValueError("Could not find a valid group block in the input grid.")

def _calculate_gap(grid: np.ndarray, pivot_index: int, group_start_index: int, group_end_index: int, group_was_before: bool) -> int:
    """Calculates the number of zeros strictly between the pivot and the group block."""
    gap = 0
    if group_was_before:
        # Gap is between group end and pivot start
        # Iterate from the position *after* the group ends up to (but not including) the pivot
        if group_end_index + 1 < pivot_index:
             gap = np.sum(grid[group_end_index + 1 : pivot_index] == 0)
    else:
        # Gap is between pivot end and group start
        # Iterate from the position *after* the pivot up to (but not including) the group start
        if pivot_index + 1 < group_start_index:
             gap = np.sum(grid[pivot_index + 1 : group_start_index] == 0)

    return int(gap) # Return as standard Python int

def _calculate_output_start(pivot_index: int, group_length: int, gap_size: int, group_was_before: bool) -> int:
    """Calculates the starting index for the group in the output grid."""
    if group_was_before:
        # Group was before pivot, move it after, preserving gap
        # Output starts at pivot_index + 1 (position after pivot) + gap_size
        output_start = pivot_index + 1 + gap_size
    else:
        # Group was after pivot, move it before, preserving gap
        # Output ends at pivot_index - 1 (position before pivot) - gap_size
        # Output starts at pivot_index - gap_size - group_length
        output_start = pivot_index - gap_size - group_length

    return int(output_start) # Return as standard Python int

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input grid.
    """
    n = len(input_grid)
    # initialize output_grid with zeros, matching input type
    output_grid = np.zeros(n, dtype=input_grid.dtype)

    # --- Locate Pivot ---
    # Find the index of the unique '2' element.
    pivot_index = _find_pivot_index(input_grid)

    # --- Place Pivot ---
    # Copy the pivot element to the same position in the output.
    output_grid[pivot_index] = 2

    # --- Locate Group ---
    # Find the contiguous block of identical non-zero, non-2 elements.
    # Get its value, start/end indices, and length.
    group_value, group_start_index, group_end_index, group_length = _find_group_info(input_grid)

    # --- Determine Relative Position (Input) ---
    # Check if the group block occurred before the pivot index in the input.
    group_was_before = group_end_index < pivot_index

    # --- Calculate Gap ---
    # Count the number of zeros strictly between the pivot and the group block in the input.
    gap_size = _calculate_gap(input_grid, pivot_index, group_start_index, group_end_index, group_was_before)

    # --- Calculate Output Position (Group) ---
    # Determine the starting index where the group block should be placed in the output,
    # based on swapping its side relative to the pivot and preserving the gap.
    output_start_index = _calculate_output_start(pivot_index, group_length, gap_size, group_was_before)
    output_end_index = output_start_index + group_length # Calculate end index (exclusive for slicing)

    # --- Place Group ---
    # Check for boundary issues before placing the group into the output grid.
    if output_start_index < 0 or output_end_index > n:
        # This case indicates an issue with logic or input assumptions if it occurs.
        raise ValueError(f"Calculated output indices [{output_start_index}:{output_end_index}] are out of bounds for grid size {n}.")

    # Copy the group value into the calculated slice of the output grid.
    output_grid[output_start_index:output_end_index] = group_value

    # --- Return Output ---
    # The output grid now contains the pivot and the repositioned group, with other elements as zero.
    return output_grid
```