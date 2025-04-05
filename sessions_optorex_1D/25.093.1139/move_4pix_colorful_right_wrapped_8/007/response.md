```python
"""
Transforms an input sequence (list or array) of 12 integers by dividing it into three consecutive blocks of 4 elements each and rearranging these blocks. The output sequence is formed by concatenating the blocks in the order: Block 3 (indices 8-11), Block 1 (indices 0-3), and Block 2 (indices 4-7).
"""

import numpy as np # numpy is imported, although standard list operations are sufficient

def transform(input_sequence):
    """
    Rearranges a sequence of 12 integers by blocks.

    Args:
        input_sequence: A list or numpy array containing 12 integers.

    Returns:
        A list containing the 12 integers rearranged according to the rule:
        Block 3, Block 1, Block 2.
    """

    # Ensure the input is treated as a list for consistent slicing and concatenation
    # This handles both list and numpy array inputs
    if isinstance(input_sequence, np.ndarray):
        input_list = input_sequence.tolist()
    else:
        # Assuming it's already list-like (e.g., a list)
        input_list = list(input_sequence) 

    # Define the size of each block
    block_size = 4

    # Verify the input list length (optional but good practice for robustness)
    if len(input_list) != 12:
        # This case shouldn't happen based on the problem description,
        # but it's good defensive programming.
        raise ValueError("Input sequence must contain exactly 12 elements.")

    # Extract the three blocks using list slicing
    # Block 1: elements at indices 0 through 3
    block_1 = input_list[0 * block_size : 1 * block_size]  # Indices 0, 1, 2, 3
    # Block 2: elements at indices 4 through 7
    block_2 = input_list[1 * block_size : 2 * block_size]  # Indices 4, 5, 6, 7
    # Block 3: elements at indices 8 through 11
    block_3 = input_list[2 * block_size : 3 * block_size]  # Indices 8, 9, 10, 11

    # Construct the output list by concatenating the blocks in the specified order: 3, 1, 2
    output_sequence = block_3 + block_1 + block_2

    # Return the rearranged sequence as a list
    # (If NumPy array output is required, convert back: np.array(output_sequence))
    return output_sequence

```