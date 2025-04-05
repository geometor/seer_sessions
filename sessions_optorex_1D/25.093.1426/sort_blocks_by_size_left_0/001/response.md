```python
import math
import collections

# Helper function to identify non-zero blocks
def _identify_non_zero_blocks(sequence):
    """
    Identifies contiguous blocks of non-zero numbers in a sequence.

    Args:
        sequence: A list of numbers.

    Returns:
        A list of lists, where each inner list is a non-zero block.
    """
    blocks = []
    current_block = []
    in_block = False
    for num in sequence:
        if num != 0:
            if not in_block:
                in_block = True
                current_block = [num]
            else:
                current_block.append(num)
        else:
            if in_block:
                blocks.append(current_block)
                in_block = False
                current_block = []
    # Add the last block if the sequence ends with non-zeros
    if in_block:
        blocks.append(current_block)
    return blocks

def transform(input_sequence_str):
    """
    Rearranges a sequence of numbers by consolidating non-zero blocks to the 
    right end, separated by single zeros. The order of blocks is reversed 
    if there are exactly two blocks and the first block has a length of 1; 
    otherwise, the original relative order is maintained. Leading zeros 
    are used for padding.
    """
    # Convert input string to list of integers
    input_sequence = [int(x) for x in input_sequence_str.split()]
    original_length = len(input_sequence)

    # 1. & 2. Identify all contiguous blocks of non-zero numbers and their original order.
    blocks = _identify_non_zero_blocks(input_sequence)

    # 3. Determine the final order for placing these blocks.
    ordered_blocks = blocks
    if len(blocks) == 2 and len(blocks[0]) == 1:
        # Reverse the order of the two blocks
        ordered_blocks = blocks[::-1] # Slicing creates a reversed copy

    # 4. Construct the core part of the output sequence.
    core_output = []
    for i, block in enumerate(ordered_blocks):
        core_output.extend(block)
        # Add a single zero separator if this is not the last block
        if i < len(ordered_blocks) - 1:
            core_output.append(0)

    # 5. Calculate the number of leading zeros needed.
    core_length = len(core_output)
    padding_zeros_count = original_length - core_length

    # 6. Create the final output sequence.
    output_sequence = [0] * padding_zeros_count + core_output

    # Convert back to string format for output
    output_str = " ".join(map(str, output_sequence))
    
    return output_str

```