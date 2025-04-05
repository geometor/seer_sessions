import math # Included standard math library, although not used in this specific solution
import numpy as np # Included standard numpy library, although not used in this specific solution

"""
Transforms a sequence of 12 digits by finding a single contiguous block of 
identical non-zero digits and shifting this entire block one position to the left. 
Positions outside the shifted block are filled with zeros.

1.  Parse the input string into a list or array of 12 integer digits.
2.  Identify the start index and the end index of the contiguous block of 
    non-zero digits within the input list.
3.  Create a new output list of 12 elements, initialized with zeros.
4.  Copy the sequence of non-zero digits (from the identified start index to 
    the end index in the input list) into the output list, starting at the 
    position `start_index - 1`.
5.  Format the output list back into a space-separated string of digits.
"""

def parse_input(input_str: str) -> list[int]:
    """Converts a space-separated string of digits into a list of integers."""
    return [int(digit) for digit in input_str.split()]

def find_nonzero_block(grid: list[int]) -> tuple[int, int]:
    """
    Finds the start and end index (inclusive) of the first contiguous 
    non-zero block in the grid. Assumes exactly one such block exists, 
    as per the examples.
    Returns (-1, -1) if no non-zero digits are found.
    """
    start_index = -1
    end_index = -1
    in_block = False
    for i, digit in enumerate(grid):
        if digit != 0:
            # Mark the start when the first non-zero digit is found
            if not in_block:
                start_index = i
                in_block = True
            # Update the end index for every non-zero digit in the block
            end_index = i
        elif in_block:
            # If we encounter a zero after being in a block, the block has ended
            break 
    return start_index, end_index

def format_output(grid: list[int]) -> str:
    """Converts a list of integers back into a space-separated string."""
    return " ".join(map(str, grid))

def transform(input_str: str) -> str:
    """
    Applies the transformation rule: shifts the non-zero block one step left.
    """
    # 1. Parse the input string into a list of integers
    input_grid = parse_input(input_str)
    n = len(input_grid) # Get the length (expected to be 12)

    # 2. Identify the start and end index of the non-zero block
    start_index, end_index = find_nonzero_block(input_grid)

    # 3. Create a new output list of the same size, initialized with zeros
    output_grid = [0] * n

    # Check if a block was actually found
    if start_index != -1:
        # Determine the new start position (one step to the left)
        # Based on examples, start_index > 0, so new_start_index >= 0
        new_start_index = start_index - 1

        # Extract the block of non-zero digits from the input
        block = input_grid[start_index : end_index + 1]
        block_len = len(block)

        # 4. Copy the block into the output grid at the new shifted position
        # This loop handles placing each digit of the block correctly
        for i in range(block_len):
            # Ensure we don't try to write past the end of the output grid
            # (although with a left shift and length 12, this shouldn't occur based on examples)
            current_output_index = new_start_index + i
            if 0 <= current_output_index < n:
                 output_grid[current_output_index] = block[i]
            # else: block is partially shifted off the left edge (not expected)

    # 5. Format the output list back into a space-separated string
    output_str = format_output(output_grid)

    return output_str
