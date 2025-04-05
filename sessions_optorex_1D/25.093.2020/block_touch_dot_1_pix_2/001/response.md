```python
"""
The transformation rule operates on a sequence of 12 single-digit integers.
It identifies the position of the number 2 as a pivot.

1.  **Locate the Pivot (2):** Find the first occurrence of the number 2 in the sequence. If 2 is not present, the sequence remains unchanged.

2.  **Check Before the Pivot:**
    *   Look immediately before the position of 2.
    *   Check if the element at `index(2) - 1` is 0.
    *   If it is 0, check if the element at `index(2) - 2` is non-zero.
    *   If both conditions are true, identify the contiguous block of non-zero numbers ending at `index(2) - 2`.
    *   Perform a right cyclic shift on the segment consisting of this non-zero block and the zero at `index(2) - 1`. For example, `[..., X, Y, Z, 0, 2, ...]` becomes `[..., 0, X, Y, Z, 2, ...]`. Only this shift is performed.

3.  **Check After the Pivot (if no shift before):**
    *   If the check *before* the pivot did not result in a shift, look immediately after the position of 2.
    *   Check if the element at `index(2) + 1` is 0.
    *   If it is 0, check if the element at `index(2) + 2` is non-zero.
    *   If both conditions are true, identify the contiguous block of non-zero numbers starting at `index(2) + 2`.
    *   Perform a left cyclic shift on the segment consisting of the zero at `index(2) + 1` and this non-zero block. For example, `[..., 2, 0, A, B, C, ...]` becomes `[..., 2, A, B, C, 0, ...]`.

4.  **No Change:** If the pivot 2 is not found, or if neither the condition before nor the condition after the pivot triggers a shift, the original sequence is returned.
"""

import collections

# Helper function to find the first index of a value
def find_first_index(seq, value):
    try:
        return seq.index(value)
    except ValueError:
        return -1

# Helper function to find contiguous non-zero block ending before a given index
def find_block_before(seq, end_index):
    if end_index < 0:
        return -1 # Invalid end index
    if seq[end_index] == 0:
        return -1 # Must end with non-zero

    start_index = end_index
    while start_index >= 0 and seq[start_index] != 0:
        start_index -= 1
    return start_index + 1 # Return the actual start index of the non-zero block

# Helper function to find contiguous non-zero block starting after a given index
def find_block_after(seq, start_index):
    if start_index >= len(seq):
        return -1 # Invalid start index
    if seq[start_index] == 0:
        return -1 # Must start with non-zero

    end_index = start_index
    while end_index < len(seq) and seq[end_index] != 0:
        end_index += 1
    return end_index - 1 # Return the actual end index of the non-zero block

def transform(input_str: str) -> str:
    """
    Applies the described cyclic shift transformation based on the position of '2'.
    """
    # Convert input string to list of integers
    input_list = [int(x) for x in input_str.split()]
    n = len(input_list)
    output_list = list(input_list) # Create a mutable copy

    # 1. Locate the Pivot (2)
    pivot_index = find_first_index(output_list, 2)

    # If 2 is not found, return the original list as a string
    if pivot_index == -1:
        return " ".join(map(str, output_list))

    shifted = False # Flag to track if a shift has occurred

    # 2. Check Before the Pivot
    # Check if pattern [non-zero block, 0] exists immediately before index(2)
    if pivot_index > 0 and output_list[pivot_index - 1] == 0:
        # Check if there's a non-zero number before the zero
        if pivot_index > 1 and output_list[pivot_index - 2] != 0:
            # Find the start of the non-zero block ending at pivot_index - 2
            block_start_index = find_block_before(output_list, pivot_index - 2)
            if block_start_index != -1:
                 # Perform right cyclic shift on the segment [block_start_index, pivot_index - 1]
                 segment_end_index = pivot_index - 1
                 segment = output_list[block_start_index : segment_end_index + 1]
                 # The zero is the last element, move it to the front
                 shifted_segment = [segment[-1]] + segment[:-1]
                 output_list[block_start_index : segment_end_index + 1] = shifted_segment
                 shifted = True

    # 3. Check After the Pivot (only if no shift happened before)
    if not shifted:
        # Check if pattern [0, non-zero block] exists immediately after index(2)
        if pivot_index < n - 1 and output_list[pivot_index + 1] == 0:
            # Check if there's a non-zero number after the zero
             if pivot_index < n - 2 and output_list[pivot_index + 2] != 0:
                 # Find the end of the non-zero block starting at pivot_index + 2
                 block_end_index = find_block_after(output_list, pivot_index + 2)
                 if block_end_index != -1:
                     # Perform left cyclic shift on the segment [pivot_index + 1, block_end_index]
                     segment_start_index = pivot_index + 1
                     segment = output_list[segment_start_index : block_end_index + 1]
                     # The zero is the first element, move it to the end
                     shifted_segment = segment[1:] + [segment[0]]
                     output_list[segment_start_index : block_end_index + 1] = shifted_segment
                     shifted = True # Not strictly necessary here, but good practice

    # Convert the result back to a space-separated string
    return " ".join(map(str, output_list))

```