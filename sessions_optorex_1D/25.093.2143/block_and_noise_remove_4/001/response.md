```python
import math
import collections

def find_nonzero_blocks(sequence):
    """
    Identifies contiguous blocks of non-zero numbers in a sequence.

    Args:
        sequence: A list of numbers.

    Returns:
        A list of dictionaries, where each dictionary represents a block
        and contains 'start', 'end', and 'length' keys.
        Returns an empty list if no non-zero blocks are found.
    """
    blocks = []
    start_index = -1
    for i, num in enumerate(sequence):
        if num != 0 and start_index == -1:
            # Start of a new block
            start_index = i
        elif (num == 0 or i == len(sequence) - 1) and start_index != -1:
            # End of the current block
            end_index = i if num != 0 else i - 1 # Adjust end index if last element is non-zero
            blocks.append({
                'start': start_index,
                'end': end_index,
                'length': end_index - start_index + 1
            })
            start_index = -1 # Reset for the next block
    return blocks

def select_longest_block(blocks):
    """
    Selects the longest block from a list of blocks.
    If there's a tie in length, selects the one with the smallest start index.

    Args:
        blocks: A list of block dictionaries (output from find_nonzero_blocks).

    Returns:
        The dictionary representing the selected block, or None if the input list is empty.
    """
    if not blocks:
        return None

    longest_block = blocks[0]
    max_length = blocks[0]['length']

    for block in blocks[1:]:
        if block['length'] > max_length:
            max_length = block['length']
            longest_block = block
        # Tie-breaking (smallest start index) is implicitly handled
        # because we only update if the current block is *strictly* longer.
        # If lengths are equal, the earlier block (with smaller index) remains selected.

    return longest_block


def transform(input_list):
    """
    Transforms the input sequence by identifying all contiguous blocks of non-zero
    integers, selecting the longest block (earliest one in case of a tie),
    and creating an output sequence containing only that block, with all other
    elements set to zero.
    """
    # 1. Identify all contiguous blocks of non-zero integers.
    blocks = find_nonzero_blocks(input_list)

    # 2. Find the block with the greatest length (earliest wins ties).
    selected_block = select_longest_block(blocks)

    # 3. Create a new sequence of the same length, filled with zeros.
    output_list = [0] * len(input_list)

    # 4. If a longest block was found, copy its elements to the output list.
    if selected_block:
        start = selected_block['start']
        end = selected_block['end']
        # Copy the elements from the selected block into the corresponding positions
        output_list[start : end + 1] = input_list[start : end + 1]

    # 5. Return the resulting sequence.
    return output_list
```