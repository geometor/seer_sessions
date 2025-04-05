```python
import numpy as np
import collections # Used for defaultdict or Counter if needed, but not strictly necessary here.

"""
Transforms a 1D NumPy array of integers based on moving elements relative to the first longest contiguous block of zeros.

1.  Identify all contiguous blocks composed entirely of zeros within the input sequence.
2.  If no blocks of zeros exist, return the original sequence unchanged.
3.  Determine the maximum length among all identified zero blocks.
4.  Select the block of zeros that has this maximum length and starts at the earliest index in the sequence (the "first longest block"). Let its start index be `block_start` and end index be `block_end`.
5.  Check if the selected block ends at the last position of the sequence (i.e., if `block_end` is the index of the last element).
6.  If the block *is* at the end of the sequence:
    a.  Find the index of the first non-zero element that appears *before* `block_start`. Let this be `target_index`. If no non-zero element exists before `block_start`, set `target_index` to 0.
    b.  Identify the element to move: it is the first zero of the selected block (the element currently at `block_start`).
    c.  Remove this element from its position (`block_start`).
    d.  Insert the removed element into the sequence at `target_index`.
7.  If the block is *not* at the end of the sequence:
    a.  Identify the element to move: it is the element immediately following the selected block (the element currently at `block_end + 1`).
    b.  Identify the target insertion index: it is the starting index of the selected block (`block_start`).
    c.  Remove the element to move from its original position (`block_end + 1`).
    d.  Insert the removed element into the sequence at the target insertion index (`block_start`).
8.  Return the modified sequence as a NumPy array.
"""


# Helper function to find all contiguous blocks of zeros
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

# Helper function to find the first longest block of zeros
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

# Helper function to find the index for insertion when the block is at the end
def find_target_insertion_index_for_end_block(seq, block_start):
    """Finds the index of the first non-zero element before block_start. Returns 0 if none found."""
    target_index = 0 # Default to index 0
    found = False
    for i in range(block_start):
        if seq[i] != 0:
            target_index = i
            found = True
            break # Found the first non-zero element
    # If no non-zero element was found before the block, target_index remains 0.
    return target_index


def transform(input_grid: np.ndarray) -> np.ndarray:
    # Convert numpy array to list for easier manipulation (pop/insert)
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

    # 3 & 4. Find the first longest block
    selected_block = find_first_longest_block(zero_blocks)
    block_start = selected_block['start']
    block_end = selected_block['end']

    # Create a mutable copy (already done by tolist())
    output_seq = seq

    # 5. Determine if the selected block is at the end of the sequence
    is_at_end = (block_end == n - 1)

    if is_at_end:
        # 6. Block is at the end
        # 6a. Find the target insertion index
        target_index = find_target_insertion_index_for_end_block(output_seq, block_start)

        # 6b. Identify the element to move (first zero of the block)
        # 6c. Remove this element from its original position
        # Check if block_start is valid before popping
        if 0 <= block_start < len(output_seq):
             moved_element = output_seq.pop(block_start)

             # 6d. Insert the removed element into the sequence at the target index
             # Adjust target_index if it was affected by the pop operation
             # If target_index < block_start, it's unaffected.
             # If target_index >= block_start, it's not possible because target must be *before* block_start
             # So, target_index is always correct relative to the state before the pop.
             output_seq.insert(target_index, moved_element)
        # Else: if block_start is somehow invalid (e.g., empty sequence edge case handled earlier), do nothing extra.

    else:
        # 7. Block is *not* at the end
        # This implies block_end + 1 < n, so an element exists after the block.

        # 7a. Identify the element to move (element immediately following block)
        move_from_index = block_end + 1

        # Check if move_from_index is valid
        if 0 <= move_from_index < len(output_seq):
            element_to_move = output_seq[move_from_index]

            # 7c. Remove this element from its original position
            output_seq.pop(move_from_index)

            # 7b & 7d. Insert the removed element at the target index (start of the block)
            # The block_start index might have shifted if move_from_index < block_start,
            # but this is not possible since move_from_index = block_end + 1 >= block_start + 1.
            # So block_start is correct relative to the list after the pop.
            output_seq.insert(block_start, element_to_move)
        # Else: If move_from_index is invalid (shouldn't happen if block is not at end and n>0), do nothing extra.

    # 8. Convert the modified list back to a NumPy array
    # Preserve original dtype if possible, otherwise default int might be okay
    output_grid = np.array(output_seq, dtype=input_grid.dtype)

    return output_grid
```