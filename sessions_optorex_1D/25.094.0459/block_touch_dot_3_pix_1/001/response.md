```python
import math
import collections

"""
Rearranges a sequence of digits based on the position of the digit '2'.
1. Finds the index of the digit '2'.
2. Finds the first contiguous block of non-zero digits (excluding '2').
3. If a block is found and separated from '2' only by zeros, the block and the intervening zeros are swapped.
4. If the block is to the left of '2', the zeros move to the left of the block.
5. If the block is to the right of '2', the zeros move to the right of the block.
6. Otherwise, the sequence remains unchanged.
"""

def find_digit(sequence, digit):
    """Finds the index of the first occurrence of a digit."""
    try:
        return sequence.index(digit)
    except ValueError:
        return -1 # Digit not found

def find_block(sequence, pivot_index):
    """
    Finds the first contiguous block of non-zero digits, excluding the pivot digit (2).
    Returns (start_index, end_index, block_value) or (None, None, None) if no block found.
    """
    block_start = -1
    block_end = -1
    block_value = None

    for i, val in enumerate(sequence):
        if val != 0 and val != 2:
            # Found the start of a potential block
            block_start = i
            block_value = val
            # Find the end of the block
            for j in range(i, len(sequence)):
                if sequence[j] == block_value:
                    block_end = j
                else:
                    break # End of contiguous block of this value
            # We only care about the first block found
            return block_start, block_end, block_value
        elif val == 2 and i == pivot_index:
            continue # Skip the pivot digit itself

    # If loop finishes without finding a block
    return None, None, None

def transform(input_sequence):
    """
    Transforms the input sequence according to the described rules.

    Args:
        input_sequence: A list of single-digit integers.

    Returns:
        A new list representing the transformed sequence.
    """
    # Make a copy to avoid modifying the original input list if no transformation occurs
    output_sequence = list(input_sequence)

    # 1. Locate the index (position) of the digit 2.
    idx_2 = find_digit(output_sequence, 2)
    if idx_2 == -1:
        return output_sequence # No '2', return original

    # 2. Find the contiguous block of non-zero digits that are not 2.
    block_start, block_end, block_value = find_block(output_sequence, idx_2)

    # If no such block exists, the sequence remains unchanged.
    if block_start is None:
        return output_sequence

    # 3. Determine the segment between the block and '2'. Check if it's all zeros.
    all_zeros = True
    if block_start > idx_2: # Block is to the right of '2'
        # Check segment between '2' (exclusive) and block_start (exclusive)
        segment_start = idx_2 + 1
        segment_end = block_start
        # Check adjacency: If block starts immediately after '2'
        if segment_start == segment_end:
             return output_sequence # Adjacent, no move needed
        for i in range(segment_start, segment_end):
            if output_sequence[i] != 0:
                all_zeros = False
                break

    elif block_end < idx_2: # Block is to the left of '2'
        # Check segment between block_end (exclusive) and '2' (exclusive)
        segment_start = block_end + 1
        segment_end = idx_2
        # Check adjacency: If block ends immediately before '2'
        if segment_start == segment_end:
            return output_sequence # Adjacent, no move needed
        for i in range(segment_start, segment_end):
            if output_sequence[i] != 0:
                all_zeros = False
                break
    else:
        # This case should ideally not happen if find_block correctly excludes '2'
        # Or if the block somehow overlaps with '2', which isn't expected
        return output_sequence


    # 4. If the segment consists entirely of zeros and block isn't adjacent:
    if all_zeros:
        # Extract parts of the sequence
        block = output_sequence[block_start : block_end + 1]

        if block_start > idx_2: # Block is RIGHT of '2'
            # Segment of zeros is between '2' and block
            zeros_segment = output_sequence[idx_2 + 1 : block_start]
            part_before_2 = output_sequence[:idx_2]
            part_after_block = output_sequence[block_end + 1 :]

            # Reconstruct: Swap block and zeros
            output_sequence = part_before_2 + [2] + block + zeros_segment + part_after_block

        elif block_end < idx_2: # Block is LEFT of '2'
            # Segment of zeros is between block and '2'
            zeros_segment = output_sequence[block_end + 1 : idx_2]
            part_before_block = output_sequence[:block_start]
            part_after_2 = output_sequence[idx_2 + 1 :]

            # Reconstruct: Swap block and zeros
            output_sequence = part_before_block + zeros_segment + block + [2] + part_after_2

    # 5. Return the potentially rearranged sequence.
    return output_sequence

```