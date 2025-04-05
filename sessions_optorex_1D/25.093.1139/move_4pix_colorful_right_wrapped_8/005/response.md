```python
"""
Transforms an input string of 12 space-separated integers by dividing the corresponding integer list into three consecutive blocks of 4 elements each and rearranging these blocks. The output string represents the rearranged list formed by concatenating the blocks in the order: Block 3 (indices 8-11), Block 1 (indices 0-3), and Block 2 (indices 4-7).
"""

import numpy as np # numpy is not strictly required but often useful for array ops

def transform(input_str: str) -> str:
    """
    Rearranges a string of 12 space-separated integers by blocks.

    Args:
        input_str: A string containing 12 space-separated integers.

    Returns:
        A string containing the 12 integers rearranged according to the rule:
        Block 3, Block 1, Block 2, joined by spaces.
    """

    # Parse the input string into a list of integers
    input_list = [int(x) for x in input_str.split()]

    # Verify the input list length (optional but good practice)
    if len(input_list) != 12:
        raise ValueError("Input string must contain exactly 12 space-separated integers.")

    # Define block size for clarity
    block_size = 4

    # Extract the three blocks using list slicing
    # Block 1: elements at indices 0 through 3
    block_1 = input_list[0 * block_size : 1 * block_size]
    # Block 2: elements at indices 4 through 7
    block_2 = input_list[1 * block_size : 2 * block_size]
    # Block 3: elements at indices 8 through 11
    block_3 = input_list[2 * block_size : 3 * block_size]

    # Construct the output list by concatenating the blocks in the order 3, 1, 2
    output_list = block_3 + block_1 + block_2

    # Format the output list back into a space-separated string
    output_str = " ".join(map(str, output_list))

    # Return the rearranged string
    return output_str

```