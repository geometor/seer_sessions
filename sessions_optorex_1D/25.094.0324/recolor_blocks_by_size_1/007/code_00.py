import numpy as np
import re # Useful for potential future pattern matching, though not strictly needed for find_blocks

"""
Transforms a sequence of digits represented by the input grid. 
The transformation involves:
1. Identifying contiguous blocks of the digit '3'.
2. Assuming exactly two such blocks exist.
3. Comparing the lengths of these two blocks (L_A for the first, L_B for the second).
4. If L_A >= L_B, the first block's digits are changed to '1' and the second to '2'.
5. If L_A < L_B, the first block's digits are changed to '2' and the second to '1'.
6. Digits '0' remain unchanged.
7. The final sequence is formatted as a space-separated string.
"""

def find_blocks(sequence, digit):
    """
    Finds contiguous blocks of a specific digit in a sequence.

    Args:
        sequence: A list of integers.
        digit: The integer digit to find blocks of.

    Returns:
        A list of tuples, where each tuple represents a block
        (start_index, end_index, length). Returns an empty list if no blocks are found.
    """
    blocks = []
    start_index = -1
    n = len(sequence)
    for i, val in enumerate(sequence):
        # Start of a potential block
        if val == digit and start_index == -1:
            start_index = i
        # End of a block (either different digit or end of sequence)
        elif val != digit and start_index != -1:
            end_index = i - 1
            length = end_index - start_index + 1
            blocks.append((start_index, end_index, length))
            start_index = -1 # Reset for the next block

    # Check if the sequence ends with the target digit block
    if start_index != -1:
        end_index = n - 1
        length = end_index - start_index + 1
        blocks.append((start_index, end_index, length))

    return blocks

def transform(input_grid: np.ndarray) -> str:
    """
    Applies the transformation rule to the input NumPy array representing a sequence.
    """
    # 1. Convert the input NumPy array (assumed 1D or flattened) into a Python list of integers.
    # Handles potential multi-dimensional arrays by flattening them.
    input_list = input_grid.flatten().tolist()

    # 2. Create a modifiable copy of this integer list for building the output.
    output_list = list(input_list)

    # 3. Scan the integer list to find all contiguous blocks of the digit '3'.
    blocks_of_3 = find_blocks(input_list, 3)

    # 4. Verify that exactly two blocks of '3's were found (as per observed examples).
    if len(blocks_of_3) == 2:
        # 5. Get the first block (Block A) and the second block (Block B).
        block_a = blocks_of_3[0] # (start_a, end_a, length_a)
        block_b = blocks_of_3[1] # (start_b, end_b, length_b)

        start_a, end_a, length_a = block_a
        start_b, end_b, length_b = block_b

        # 6. Compare the length of Block A (L_A) with the length of Block B (L_B).
        if length_a >= length_b:
            # 7a. If L_A >= L_B: Update Block A indices to 1, Block B indices to 2.
            for i in range(start_a, end_a + 1):
                output_list[i] = 1
            for i in range(start_b, end_b + 1):
                output_list[i] = 2
        else:
            # 7b. If L_A < L_B: Update Block A indices to 2, Block B indices to 1.
            for i in range(start_a, end_a + 1):
                output_list[i] = 2
            for i in range(start_b, end_b + 1):
                output_list[i] = 1
    # Note: If not exactly two blocks are found, the output_list currently remains
    # unchanged from the input_list, effectively preserving '0's and any '3's
    # that didn't fit the two-block pattern based on the examples.

    # 8. Convert the integers in the modified output list back into strings.
    # 9. Join these digit strings with spaces to form the final output string.
    output_str = " ".join(map(str, output_list))

    # Return the final formatted string
    return output_str