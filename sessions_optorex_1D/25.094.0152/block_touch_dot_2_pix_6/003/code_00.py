import numpy as np # Using numpy for potential array operations if needed, though base lists work too.
from typing import List # Explicit typing for clarity

"""
Transformation Rule Natural Language Description:

1.  Accept the input sequence (a list or array of 12 integers).
2.  Create a new output sequence of 12 zeros.
3.  Find the index (`pivot_index`) of the integer `2` in the input sequence.
4.  Place the integer `2` at the `pivot_index` in the output sequence.
5.  Scan the input sequence to find the *first* contiguous block of non-zero integers, excluding the integer at `pivot_index`. Record its starting index (`block_start`), ending index (`block_end`), and the list of values (`block_values`).
6.  If no such data block is found, return the output sequence (which currently contains only the `2` and zeros).
7.  Determine the relative position of the block with respect to the `pivot_index`:
    *   If `block_end < pivot_index`, the block is "Left". Calculate `gap = pivot_index - block_end - 1`.
    *   If `block_start > pivot_index`, the block is "Right". Calculate `gap = block_start - pivot_index - 1`.
    *   Otherwise (adjacent), the `gap = 0`.
8.  Calculate the `shift_amount`:
    *   If `gap == 0`, `shift_amount = 0`.
    *   If `gap == 1`, `shift_amount = 1`.
    *   If `gap > 1`, `shift_amount = 2`.
9.  Calculate the `new_block_start` index for the output sequence:
    *   If the block was "Left", `new_block_start = block_start + shift_amount`.
    *   If the block was "Right", `new_block_start = block_start - shift_amount`.
    *   If the block was "Adjacent" (`gap == 0`), `new_block_start = block_start`.
10. Iterate through the `block_values`. For each value, calculate its target index in the output sequence (starting from `new_block_start`). If the target index is *not* equal to `pivot_index`, place the value at that target index in the output sequence.
11. Return the completed output sequence.
"""

def find_pivot(sequence: List[int]) -> int:
    """Finds the index of the pivot element (2). Returns -1 if not found."""
    try:
        # Use list.index() for efficiency
        return sequence.index(2)
    except ValueError:
        return -1 # Pivot not found

def find_data_block(sequence: List[int], pivot_index: int) -> tuple:
    """
    Finds the first contiguous block of non-zero, non-pivot integers.
    Returns (start_index, end_index, values) or (None, None, None) if no block found.
    """
    block_start = -1
    block_values = []
    n = len(sequence)

    for i, val in enumerate(sequence):
        # Check if the current element qualifies as part of the data block
        is_block_element = (val != 0 and i != pivot_index)

        if is_block_element and block_start == -1:
            # Start of a potential block
            block_start = i
            block_values.append(val)
        elif is_block_element and block_start != -1:
            # Continuing an existing block
            block_values.append(val)
        elif not is_block_element and block_start != -1:
            # End of the block is detected (current element is 0 or pivot)
            block_end = i - 1
            return block_start, block_end, block_values

    # Handle case where block runs to the very end of the sequence
    if block_start != -1:
        block_end = n - 1
        return block_start, block_end, block_values

    # No block was found
    return None, None, None


def transform(input_sequence: List[int]) -> List[int]:
    """
    Applies the transformation rule to the input sequence.
    """
    n = len(input_sequence)
    if n != 12:
        # Handle unexpected input length if necessary, though examples are fixed length
        print(f"Warning: Input sequence length is {n}, expected 12.")
        # Decide on behavior: return input, raise error, or proceed? Proceeding for now.
        pass 

    # 1. Initialize output sequence with zeros
    output_sequence = [0] * n

    # 2. Find the pivot index
    pivot_index = find_pivot(input_sequence)
    if pivot_index == -1:
        # If pivot '2' is missing, return the initialized (all zeros) or original sequence?
        # Based on examples, pivot is always present. Let's return original if missing.
        print("Warning: Pivot '2' not found in input sequence.")
        return list(input_sequence) # Return a copy

    # 3. Place pivot in the output sequence (it never moves)
    output_sequence[pivot_index] = 2

    # 4. Find the data block
    block_start, block_end, block_values = find_data_block(input_sequence, pivot_index)

    # 5. If no data block found, the transformation is complete
    if block_start is None:
        return output_sequence

    # 6. Determine relative position and calculate gap
    gap = 0
    relative_position = "Adjacent" # Default assumption
    if block_end < pivot_index:
        relative_position = "Left"
        gap = pivot_index - block_end - 1
    elif block_start > pivot_index:
        relative_position = "Right"
        gap = block_start - pivot_index - 1

    # Ensure gap isn't negative (can happen if adjacent before max)
    gap = max(0, gap)

    # 7. Calculate shift amount based on gap
    shift_amount = 0
    if gap == 1:
        shift_amount = 1
    elif gap > 1:
        shift_amount = 2

    # 8. Calculate new block starting index
    new_block_start = block_start # Start with original position
    if relative_position == "Left":
        new_block_start += shift_amount
    elif relative_position == "Right":
        new_block_start -= shift_amount
    # No change if Adjacent (shift_amount is 0)

    # 9. Place the shifted data block into the output sequence
    current_output_idx = new_block_start
    for val in block_values:
        # Check bounds and avoid overwriting the pivot
        if 0 <= current_output_idx < n:
            if current_output_idx != pivot_index:
                 output_sequence[current_output_idx] = val
            # If the target IS the pivot index, the value is simply skipped/overwritten by the pivot later (or already placed)
        #else:
             # Handle cases where shift pushes block out of bounds (shouldn't happen with rule)
             # print(f"Warning: Index {current_output_idx} out of bounds for value {val}.")
             # pass # Skip placing value if out of bounds

        current_output_idx += 1 # Move to next position for the next value in the block

    # 10. Return the final transformed sequence
    return output_sequence