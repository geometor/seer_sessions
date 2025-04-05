import numpy as np

def transform(input_str: str) -> str:
    """
    Takes an input list of 12 integers, represented as a space-separated string.
    Divides the input list into three consecutive blocks of 4 elements each.
    Constructs the output list by concatenating these blocks in the order:
    Block 3, then Block 1, then Block 2.
    Returns the output list as a space-separated string.
    """

    # Parse the input string into a list of integers
    input_list = [int(x) for x in input_str.split()]

    # Define block size
    block_size = 4
    num_blocks = len(input_list) // block_size

    # Ensure the input list length is a multiple of block_size
    if len(input_list) % block_size != 0:
        raise ValueError("Input list length must be a multiple of block size (4)")

    # Divide the input list into three blocks
    block_1 = input_list[0 * block_size : 1 * block_size] # Elements 0-3
    block_2 = input_list[1 * block_size : 2 * block_size] # Elements 4-7
    block_3 = input_list[2 * block_size : 3 * block_size] # Elements 8-11

    # Construct the output list by concatenating blocks in the order 3, 1, 2
    output_list = block_3 + block_1 + block_2

    # Format the output list back into a space-separated string
    output_str = " ".join(map(str, output_list))

    return output_str
