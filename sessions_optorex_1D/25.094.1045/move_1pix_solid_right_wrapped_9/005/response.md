```python
import numpy as np

"""
Transforms a 1D NumPy array of integers based on swapping elements relative to the longest contiguous block of zeros.

1.  Identify all contiguous blocks of zeros within the input sequence.
2.  If no blocks of zeros are found, return the original sequence.
3.  Find the block(s) with the greatest length. If there is more than one block with the maximum length, select the one that starts at the earliest index (the first longest block).
4.  Determine if this selected block ends at the last index of the sequence.
5.  If the block is at the end of the sequence:
    a.  Search the sequence *before* the start of the block for the first non-zero element (i.e., find the smallest index `i` such that `i < block_start_index` and `sequence[i] != 0`).
    b.  If such a non-zero element is found at index `j`:
        i.  Identify the first zero of the selected block (at index `block_start_index`).
        ii. Swap the element at index `j` with the element at index `block_start_index`.
    c.  If no non-zero element is found before the block, make no changes to the sequence.
6.  If the block is *not* at the end of the sequence:
    a.  Identify the element immediately following the block (at index `block_end_index + 1`).
    b.  Identify the first zero of the selected block (at index `block_start_index`).
    c.  Swap the element immediately following the block with the first zero of the block.
7.  Return the modified sequence as a NumPy array.
"""

def find_zero_blocks(seq):
    """Finds all contiguous blocks of zeros in a list."""
    blocks = []
    start_index = -1
    n = len(seq)
    for i, val in enumerate(seq):
        if val == 0 and start_index == -1:
            # Start of a potential block
            start_index = i
        elif val != 0 and start_index != -1:
            # End of the current block
            end_index = i - 1
            blocks.append({'start': start_index, 'end': end_index, 'len': end_index - start_index + 1})
            start_index = -1 # Reset for next block

    # Check if the sequence ends with a block of zeros
    if start_index != -1:
        end_index = n - 1
        blocks.append({'start': start_index, 'end': end_index, 'len': end_index - start_index + 1})

    return blocks

def find_first_longest_block(blocks):
    """Finds the longest block of zeros from a list of blocks, selecting the first one in case of a tie."""
    if not blocks:
        return None

    max_len = 0
    # Find the maximum length among all blocks
    for block in blocks:
        if block['len'] > max_len:
            max_len = block['len']

    # Filter blocks that have the maximum length
    longest_blocks = [block for block in blocks if block['len'] == max_len]

    # Select the one with the smallest start index if there are multiple longest blocks
    selected_block = min(longest_blocks, key=lambda b: b['start'])
    return selected_block

def find_first_preceding_non_zero_index(seq, block_start):
    """Finds the index of the first non-zero element before the block_start index."""
    target_index = -1 # Return -1 if no non-zero element is found
    for i in range(block_start):
        if seq[i] != 0:
            target_index = i
            break # Found the first non-zero element
    return target_index

def transform(input_grid: np.ndarray) -> np.ndarray:
    # Convert numpy array to list for easier manipulation (swapping)
    seq = input_grid.tolist()
    n = len(seq)

    # Handle empty input
    if n == 0:
        return input_grid # Return original empty array

    # 1. Identify all contiguous blocks of zeros
    zero_blocks = find_zero_blocks(seq)

    # 2. Handle case where there are no zeros
    if not zero_blocks:
        return input_grid # Return original array if no zeros

    # 3. Find the longest block (select first one if tie)
    selected_block = find_first_longest_block(zero_blocks)
    block_start = selected_block['start']
    block_end = selected_block['end']

    # Create a mutable copy (already done by tolist())
    output_seq = seq

    # 4. Determine if the selected block is at the end of the sequence
    is_at_end = (block_end == n - 1)

    if is_at_end:
        # 5. Block is at the end
        # 5a. Find the index of the first non-zero element before the block
        first_preceding_non_zero_idx = find_first_preceding_non_zero_index(output_seq, block_start)

        # 5b. If found, swap it with the first zero of the block
        if first_preceding_non_zero_idx != -1:
            # Swap elements
            output_seq[block_start], output_seq[first_preceding_non_zero_idx] = \
                output_seq[first_preceding_non_zero_idx], output_seq[block_start]
        # 5c. If no preceding non-zero found, do nothing.

    else:
        # 6. Block is *not* at the end
        # This implies block_end + 1 < n, so an element exists after the block.

        # 6a. Identify the index of the element immediately following the block
        following_idx = block_end + 1

        # 6b & 6c. Swap the first zero of the block with the following element
        output_seq[block_start], output_seq[following_idx] = \
            output_seq[following_idx], output_seq[block_start]

    # 7. Convert the modified list back to a NumPy array
    output_grid = np.array(output_seq, dtype=input_grid.dtype) # Preserve original dtype

    return output_grid

```