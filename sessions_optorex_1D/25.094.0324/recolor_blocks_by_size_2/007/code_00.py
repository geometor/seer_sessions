import numpy as np
from typing import List, Dict, Tuple

"""
Transforms a 1D sequence of integers (0s and 3s) based on comparing the lengths of contiguous blocks of '3's.

1.  Identifies the two contiguous blocks (runs) of the integer '3' in the input sequence. It assumes exactly two such blocks exist.
2.  Compares the lengths of the first block (Block1) and the second block (Block2).
3.  If the length of Block1 is strictly greater than the length of Block2:
    - Integers in Block1 are replaced with '1'.
    - Integers in Block2 are replaced with '2'.
4.  Otherwise (if the length of Block1 is less than or equal to the length of Block2):
    - Integers in Block1 are replaced with '2'.
    - Integers in Block2 are replaced with '1'.
5.  Integers originally '0' remain unchanged.
6.  Returns the modified sequence as a numpy array.
"""

# Helper function to find contiguous blocks of a specific value
def find_blocks(data: List[int], value: int) -> List[Dict[str, int]]:
    """
    Finds contiguous blocks of a specific value in a list of integers.

    Args:
        data (List[int]): The list of integers to search within.
        value (int): The integer value to find blocks of.

    Returns:
        List[Dict[str, int]]: A list of dictionaries, where each dictionary
                               represents a block and contains 'start' (index),
                               'end' (index), and 'length'. Returns an empty
                               list if no blocks are found.
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
            start_index = -1 # Reset start index

    # Handle case where a block extends to the very end of the list
    if in_block:
        end_index = len(data) - 1
        length = end_index - start_index + 1
        blocks.append({'start': start_index, 'end': end_index, 'length': length})

    return blocks

def transform(input_sequence: np.ndarray) -> np.ndarray:
    """
    Applies the block-length comparison transformation rule to the input sequence.
    """
    # Convert numpy array to list for easier processing with helper function
    input_list = input_sequence.tolist()

    # Initialize output_list as a copy of the input list
    # This ensures elements not part of '3' blocks (like '0') are preserved by default
    output_list = list(input_list)

    # Step 1 & 2: Identify the two contiguous blocks of '3's
    blocks_of_3 = find_blocks(input_list, 3)

    # Assume exactly two blocks exist based on examples and proceed with logic
    if len(blocks_of_3) == 2:
        first_block = blocks_of_3[0]
        second_block = blocks_of_3[1]

        # Step 3 & 4: Compare lengths and determine replacement values
        if first_block['length'] > second_block['length']:
            # First block is longer: Block1 -> 1, Block2 -> 2
            val_for_block1 = 1
            val_for_block2 = 2
        else:
            # First block is shorter or equal: Block1 -> 2, Block2 -> 1
            val_for_block1 = 2
            val_for_block2 = 1

        # Step 3 & 4 (cont.): Apply transformations to the output list for the first block
        for i in range(first_block['start'], first_block['end'] + 1):
             if 0 <= i < len(output_list): # Basic bounds check
                output_list[i] = val_for_block1

        # Step 3 & 4 (cont.): Apply transformations to the output list for the second block
        for i in range(second_block['start'], second_block['end'] + 1):
             if 0 <= i < len(output_list): # Basic bounds check
                output_list[i] = val_for_block2

    # If not exactly two blocks are found, the original sequence (copy) is returned implicitly.
    # Step 5 (keeping '0's) is handled by initializing output_list as a copy and only modifying '3' blocks.

    # Step 6: Convert the result back to a numpy array with integer type
    output_sequence = np.array(output_list, dtype=int)

    return output_sequence