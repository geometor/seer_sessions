import math
import collections

"""
The transformation rule takes a sequence of 12 integers as input. 
This sequence contains exactly two non-overlapping, contiguous blocks of a single non-zero 'target' digit, with the rest being zeros.
The transformation rearranges these two blocks at the beginning of the output sequence, separated by a single zero. 
Let the first block encountered in the input be B1 and the second be B2.
If the length of B1 is strictly greater than the length of B2, the output starts with B2, then a zero, then B1.
Otherwise (if the length of B1 is less than or equal to the length of B2), the output starts with B1, then a zero, then B2.
The remaining positions in the 12-element output sequence are filled with zeros.
"""

def find_target_digit(nums):
    """Finds the non-zero digit in the list."""
    for num in nums:
        if num != 0:
            return num
    # This case should ideally not be reached based on problem description
    # If input is all zeros, return 0, let transform handle it.
    return 0

def find_digit_blocks(nums, target_digit):
    """Finds contiguous blocks of the target_digit in the list."""
    blocks = []
    current_block = []
    in_block = False
    for num in nums:
        if num == target_digit:
            # Start or continue a block
            current_block.append(num)
            in_block = True
        else:
            # End of a block (if we were in one)
            if in_block:
                blocks.append(list(current_block)) # Append a copy
                current_block = []
                in_block = False
    # Check if the last element was part of a block
    if in_block:
        blocks.append(list(current_block))
        
    # Expecting exactly two blocks based on the problem description
    if len(blocks) == 2:
        return blocks[0], blocks[1]
    elif len(blocks) == 1 and target_digit != 0:
         # Handle case where maybe only one block exists? 
         # Based on observation, always two blocks. If only one, maybe treat the second as empty?
         # Let's stick to the 2-block assumption from observation.
         # print(f"Warning: Found only one block for target {target_digit}.")
         return blocks[0], [] # Or raise an error? Returning empty list for B2.
    elif len(blocks) == 0 and target_digit != 0:
        # print(f"Warning: Found no blocks for target {target_digit}.")
        return [], [] # Should not happen if target_digit is non-zero
    elif target_digit == 0:
        return [], [] # No blocks if target is 0
    else:
        # print(f"Warning: Found {len(blocks)} blocks, expected 2.")
        # Fallback or error? Let's assume the first two are the relevant ones if more exist.
        # Sticking to the 2-block assumption based on examples.
        # This path indicates an input format violation if examples are representative.
        # We will proceed assuming exactly two blocks are found.
         return blocks[0], blocks[1]


def transform(input_str: str) -> str:
    """
    Applies the transformation rule to the input string.
    
    Args:
        input_str: A string representing 12 space-separated integers.

    Returns:
        A string representing the transformed 12 space-separated integers.
    """
    # Parse the input string into a list of integers
    input_nums = [int(x) for x in input_str.split()]
    output_size = 12
    
    # Handle edge case: input might be all zeros (though not in examples)
    target = find_target_digit(input_nums)
    if target == 0:
        return " ".join(['0'] * output_size)

    # Find the two blocks of the target digit
    # Assumes exactly two blocks exist based on observations
    block1, block2 = find_digit_blocks(input_nums, target)

    # Determine the order based on block lengths
    output_prefix = []
    if len(block1) > len(block2):
        # If B1 is longer, output is B2, 0, B1
        output_prefix.extend(block2)
        output_prefix.append(0)
        output_prefix.extend(block1)
    else:
        # If B1 is shorter or equal, output is B1, 0, B2
        output_prefix.extend(block1)
        output_prefix.append(0)
        output_prefix.extend(block2)

    # Construct the final output list
    output_nums = output_prefix[:] # Make a copy

    # Pad the rest with zeros
    padding_needed = output_size - len(output_nums)
    if padding_needed > 0:
        output_nums.extend([0] * padding_needed)
    elif padding_needed < 0:
        # This implies the combined blocks + zero exceeded 12, shouldn't happen with input length 12
        # Truncate if necessary, although it signals an issue.
        output_nums = output_nums[:output_size]

    # Convert the output list back to a space-separated string
    return " ".join(map(str, output_nums))
