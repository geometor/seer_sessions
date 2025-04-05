```python
import math
from typing import List, Tuple

# Helper function to parse the input string into a list of integers
def parse_input(input_str: str) -> List[int]:
    """Converts a space-separated string of digits into a list of integers."""
    return [int(digit) for digit in input_str.split()]

# Helper function to identify blocks of consecutive identical digits
def identify_blocks(digits: List[int]) -> List[Tuple[int, int]]:
    """
    Identifies contiguous blocks of identical digits.
    Returns a list of tuples, where each tuple is (digit, length).
    Example: [0, 0, 5, 5, 5, 0] -> [(0, 2), (5, 3), (0, 1)]
    """
    if not digits:
        return []

    blocks = []
    current_digit = digits[0]
    current_length = 0
    for digit in digits:
        if digit == current_digit:
            current_length += 1
        else:
            blocks.append((current_digit, current_length))
            current_digit = digit
            current_length = 1
    # Append the last block
    blocks.append((current_digit, current_length))
    return blocks

# Helper function to reconstruct the sequence string from blocks
def reconstruct_sequence(blocks: List[Tuple[int, int]]) -> str:
    """
    Reconstructs the space-separated digit string from a list of blocks.
    Example: [(0, 2), (5, 3), (0, 1)] -> "0 0 5 5 5 0"
    """
    output_digits = []
    for digit, length in blocks:
        output_digits.extend([str(digit)] * length)
    return " ".join(output_digits)

def transform(input_str: str) -> str:
    """
    Transforms the input sequence based on the observed pattern.
    The pattern involves finding the first and last blocks of a specific digit
    that are separated only by blocks of a different digit. If such a pattern
    is found, one element (digit) is moved from the first block to the end
    of the last block. This process happens at most once per input string.

    1. Parse the input string into a list of digits.
    2. Identify contiguous blocks of identical digits (value, length).
    3. Iterate through the unique digits present in the blocks.
    4. For each unique digit, find the index of the first block and the last block containing that digit.
    5. Check if these first and last blocks are distinct and separated only by blocks of different digits.
    6. If the condition is met:
        a. Decrease the length of the first block by 1.
        b. Increase the length of the last block by 1.
        c. Remove any block whose length becomes 0.
        d. Stop searching (assume only one transfer occurs).
    7. Reconstruct the output sequence string from the modified blocks.
    """
    # 1. Parse input
    digits = parse_input(input_str)
    if not digits:
        return ""

    # 2. Identify blocks
    blocks = identify_blocks(digits)

    unique_digits = sorted(list(set(d[0] for d in blocks))) # Process digits in a consistent order if needed
    transformed = False
    new_blocks = list(blocks) # Work on a copy

    # 3. Iterate through unique digits
    for digit_to_check in unique_digits:
        if transformed: # Optimization: Stop after the first successful transformation
            break

        # 4. Find first and last block indices for the current digit
        first_idx = -1
        last_idx = -1
        indices = [i for i, block in enumerate(new_blocks) if block[0] == digit_to_check]

        if len(indices) >= 2:
            first_idx = indices[0]
            last_idx = indices[-1]

        # 5. Check if distinct and separated correctly
        if first_idx != -1 and first_idx < last_idx:
            is_separated_correctly = True
            # Check all blocks *between* the first and last
            for i in range(first_idx + 1, last_idx):
                if new_blocks[i][0] == digit_to_check:
                    is_separated_correctly = False
                    break

            # 6. If conditions met, perform the transfer
            if is_separated_correctly:
                # a. Decrease length of first block
                first_block_val, first_block_len = new_blocks[first_idx]
                new_blocks[first_idx] = (first_block_val, first_block_len - 1)

                # b. Increase length of last block
                last_block_val, last_block_len = new_blocks[last_idx]
                new_blocks[last_idx] = (last_block_val, last_block_len + 1)

                # c. Remove blocks with length 0
                new_blocks = [b for b in new_blocks if b[1] > 0]

                # d. Mark as transformed and stop searching
                transformed = True
                # Note: The loop for unique_digits will break in the next iteration

    # 7. Reconstruct sequence
    output_str = reconstruct_sequence(new_blocks)

    return output_str

```