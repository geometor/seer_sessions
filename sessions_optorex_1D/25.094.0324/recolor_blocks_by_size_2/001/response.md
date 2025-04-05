```python
import re

"""
Transforms a sequence of digits based on contiguous blocks of '3's.

1.  Parses the input string into a list of integers.
2.  Identifies all contiguous blocks (runs) of the digit '3' in the input list.
3.  Assumes exactly two blocks of '3's exist based on the provided examples.
4.  Checks the length of the first block of '3's.
5.  Creates an output list, initially copying the input list.
6.  If the first block's length is greater than 2:
    - Replaces digits in the first block's positions with '1'.
    - Replaces digits in the second block's positions with '2'.
7.  Otherwise (if the first block's length is 2 or less):
    - Replaces digits in the first block's positions with '2'.
    - Replaces digits in the second block's positions with '1'.
8.  Digits originally '0' remain '0'.
9.  Formats the transformed list back into a space-separated string.
"""

def find_blocks(data, value):
    """
    Finds contiguous blocks of a specific value in a list.

    Args:
        data (list): The list of values (e.g., integers) to search within.
        value: The value to find blocks of.

    Returns:
        list: A list of dictionaries, where each dictionary represents a block
              and contains 'start' (index), 'end' (index), and 'length'.
              Returns an empty list if no blocks are found.
    """
    blocks = []
    in_block = False
    start_index = -1
    for i, val in enumerate(data):
        # Start of a new block
        if val == value and not in_block:
            in_block = True
            start_index = i
        # End of the current block (value changed)
        elif val != value and in_block:
            end_index = i - 1
            length = end_index - start_index + 1
            blocks.append({'start': start_index, 'end': end_index, 'length': length})
            in_block = False
    # Handle case where a block extends to the very end of the list
    if in_block:
        end_index = len(data) - 1
        length = end_index - start_index + 1
        blocks.append({'start': start_index, 'end': end_index, 'length': length})
    return blocks

def transform(input_str):
    """
    Applies the transformation rule to the input string.
    """
    # 1. Parse input string into a list of integers
    input_list = [int(x) for x in input_str.split()]

    # 2. Find all contiguous blocks of '3's
    blocks_of_3 = find_blocks(input_list, 3)

    # 3. Initialize the output list as a copy of the input
    output_list = list(input_list)

    # 4. Apply the transformation logic
    # Check if exactly two blocks were found, as per observed examples
    if len(blocks_of_3) == 2:
        first_block = blocks_of_3[0]
        second_block = blocks_of_3[1]

        # 5. Determine the transformation values based on the length of the first block
        if first_block['length'] > 2:
            val_for_block1 = 1
            val_for_block2 = 2
        else:  # length is 2 or less
            val_for_block1 = 2
            val_for_block2 = 1

        # 6. Apply transformations to the output list for both blocks
        for i in range(first_block['start'], first_block['end'] + 1):
            output_list[i] = val_for_block1
        for i in range(second_block['start'], second_block['end'] + 1):
            output_list[i] = val_for_block2
            
    # Note: The logic implicitly handles step 8 (Zeros remain unchanged)
    # because we only modify the positions corresponding to the blocks of '3's.
    # Also assumes based on examples that there are always exactly two blocks of 3s.

    # 9. Convert the output list back to a space-separated string
    output_str = " ".join(map(str, output_list))

    return output_str

```