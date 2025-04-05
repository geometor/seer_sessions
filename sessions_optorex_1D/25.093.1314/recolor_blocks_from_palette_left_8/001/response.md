```python
import re

"""
Replace contiguous blocks of the digit '5' in the first 10 elements of a 12-element 
integer sequence based on the values of the last two elements. If one block of '5's 
exists, replace its elements with the value at index 11. If two blocks exist, 
replace the first block's elements with the value at index 10 and the second block's 
elements with the value at index 11. Elements other than '5' in the first 10 
positions, and the elements at indices 10 and 11, remain unchanged.
"""

def find_five_blocks(sequence):
    """
    Finds contiguous blocks of the digit 5 in the first 10 elements.

    Args:
        sequence: The input list of integers (length 12).

    Returns:
        A list of tuples, where each tuple represents a block
        and contains (start_index, end_index_exclusive).
    """
    blocks = []
    in_block = False
    start_index = -1
    # Iterate through the first 10 elements
    for i in range(10):
        if sequence[i] == 5 and not in_block:
            # Start of a new block
            in_block = True
            start_index = i
        elif sequence[i] != 5 and in_block:
            # End of a block
            in_block = False
            blocks.append((start_index, i))
            start_index = -1

    # Handle case where a block extends to the end (index 9)
    if in_block:
        blocks.append((start_index, 10))

    return blocks

def transform(input_sequence):
    """
    Transforms the input sequence according to the rules derived from examples.

    Args:
        input_sequence: A list of 12 integers.

    Returns:
        A list of 12 integers representing the transformed sequence.
    """
    # Initialize output_sequence as a copy of the input
    output_sequence = list(input_sequence)

    # Extract control values
    val1 = input_sequence[10]
    val2 = input_sequence[11]

    # Find blocks of '5's in the first 10 elements
    five_blocks = find_five_blocks(input_sequence)

    # Apply transformations based on the number of blocks found
    if len(five_blocks) == 1:
        # If one block, replace '5's with val2
        start, end = five_blocks[0]
        for i in range(start, end):
            output_sequence[i] = val2
    elif len(five_blocks) == 2:
        # If two blocks, replace first block with val1, second with val2
        # First block
        start1, end1 = five_blocks[0]
        for i in range(start1, end1):
            output_sequence[i] = val1
        # Second block
        start2, end2 = five_blocks[1]
        for i in range(start2, end2):
            output_sequence[i] = val2

    # The elements at index 10 and 11, and non-'5' elements in 0-9,
    # are already correct due to the initial copy.

    return output_sequence

```