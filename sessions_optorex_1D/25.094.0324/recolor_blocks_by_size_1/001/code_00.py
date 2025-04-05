import re

"""
Transforms a sequence of digits by finding contiguous blocks of '3's. 
If there are exactly two blocks, compares their lengths. 
If the first block's length is greater than or equal to the second block's length, 
the first block becomes '1's and the second becomes '2's. 
Otherwise, the first block becomes '2's and the second becomes '1's. 
Digits '0' remain unchanged.
"""

def find_blocks(sequence, digit):
    """
    Finds contiguous blocks of a specific digit in a sequence.

    Args:
        sequence: A list of integers.
        digit: The integer digit to find blocks of.

    Returns:
        A list of tuples, where each tuple represents a block
        (start_index, end_index, length).
    """
    blocks = []
    start_index = -1
    for i, val in enumerate(sequence):
        if val == digit:
            if start_index == -1:
                start_index = i
        elif start_index != -1:
            # Block ended at the previous index
            end_index = i - 1
            length = end_index - start_index + 1
            blocks.append((start_index, end_index, length))
            start_index = -1 # Reset for the next block

    # Check if the sequence ends with a block
    if start_index != -1:
        end_index = len(sequence) - 1
        length = end_index - start_index + 1
        blocks.append((start_index, end_index, length))

    return blocks

def transform(input_str: str) -> str:
    """
    Applies the transformation rule to the input string.
    """
    # 1. Parse the input sequence into digits.
    input_digits = [int(d) for d in input_str.split()]

    # 2. Initialize an output sequence identical to the input sequence.
    output_digits = list(input_digits)

    # 3. Find all contiguous blocks of the digit '3'.
    blocks_of_3 = find_blocks(input_digits, 3)

    # 4. Assume exactly two blocks are found and apply the transformation logic.
    if len(blocks_of_3) == 2:
        block_a = blocks_of_3[0] # (start_a, end_a, length_a)
        block_b = blocks_of_3[1] # (start_b, end_b, length_b)

        start_a, end_a, length_a = block_a
        start_b, end_b, length_b = block_b

        # 5. Compare the lengths of Block A and Block B.
        if length_a >= length_b:
            # 6a. Replace Block A with '1's and Block B with '2's.
            for i in range(start_a, end_a + 1):
                output_digits[i] = 1
            for i in range(start_b, end_b + 1):
                output_digits[i] = 2
        else:
            # 6b. Replace Block A with '2's and Block B with '1's.
            for i in range(start_a, end_a + 1):
                output_digits[i] = 2
            for i in range(start_b, end_b + 1):
                output_digits[i] = 1
    # Handle cases with not exactly two blocks if necessary, although
    # based on examples, we assume two blocks. If not 2 blocks,
    # the output currently remains the same as the input for non-'0' digits.

    # 7. Format the output sequence as space-separated digits.
    output_str = " ".join(map(str, output_digits))

    return output_str
