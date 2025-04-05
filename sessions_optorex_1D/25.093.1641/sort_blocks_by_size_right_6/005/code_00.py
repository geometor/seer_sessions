"""
Transforms an input sequence of 12 integers based on the following rules:
1. Identify the single non-zero 'target digit' present in the input. If only zeros exist, return a sequence of 12 zeros.
2. Locate the two separate, contiguous blocks of this target digit. Let the first occurring block be Block1 and the second be Block2.
3. Compare the lengths of Block1 and Block2.
4. If Block1 is strictly longer than Block2, the output starts with Block2, followed by a single 0, then Block1.
5. Otherwise (if Block1 is shorter or equal in length to Block2), the output starts with Block1, followed by a single 0, then Block2.
6. Pad the resulting sequence with trailing zeros to ensure the final output sequence has a length of 12.
"""

import re
import numpy as np # Import numpy for potential input type handling

def find_target_digit(nums: list) -> int:
    """Finds the first non-zero digit in the list."""
    for num in nums:
        if num != 0:
            return num
    return 0 # Return 0 if all elements are zero

def find_digit_blocks(nums: list, target_digit: int) -> tuple[list, list]:
    """
    Finds the two contiguous blocks of the target_digit in the list using regex.
    Returns two lists representing the blocks (or empty lists if not found).
    """
    if target_digit == 0:
        return [], []
    
    # Convert the list to a string representation for regex matching
    text_repr = "".join(map(str, nums))
    # Create a pattern to find consecutive occurrences of the target digit
    pattern = f"({target_digit}+)" 
    
    blocks_as_lists = []
    # Find all non-overlapping matches
    matches = re.finditer(pattern, text_repr)
    
    for match in matches:
        # Convert the matched string back to a list of integers
        block_str = match.group(1)
        blocks_as_lists.append([int(digit) for digit in block_str])
        
    # Expecting exactly two blocks based on the problem description
    if len(blocks_as_lists) == 2:
        return blocks_as_lists[0], blocks_as_lists[1]
    elif len(blocks_as_lists) == 1:
         # If only one block, return it as the first block and an empty second block
        return blocks_as_lists[0], [] 
    else:
        # If zero or more than two blocks found, return empty lists (signals an issue or edge case)
        return [], [] 

def transform(input_sequence) -> list:
    """
    Applies the transformation rule to the input sequence.
    
    Args:
        input_sequence: A list or numpy array of 12 integers.

    Returns:
        A list representing the transformed 12 integers.
    """
    # Define the target output size
    output_size = 12

    # --- Step 0: Ensure input is a list ---
    if isinstance(input_sequence, np.ndarray):
        # If input is a numpy array, convert it to a list
        # Flatten in case it's misinterpreted as 2D (e.g., shape (1, 12))
        input_nums = input_sequence.flatten().tolist() 
    else:
        # Assume it's already list-like (e.g., list, tuple) and convert to list
        input_nums = list(input_sequence) 
        
    # Basic validation for input length
    if len(input_nums) != output_size:
        # Handle error or return default if input size is wrong
        # For now, returning zeros, but an error might be better
        # print(f"Warning: Input sequence length is {len(input_nums)}, expected {output_size}.")
        return [0] * output_size 

    # --- Step 1: Identify the Target Digit ---
    target = find_target_digit(input_nums)

    # --- Handle All-Zeros Case ---
    if target == 0:
        # If the target digit is 0, the input was all zeros
        return [0] * output_size

    # --- Step 2: Locate Block1 and Block2 ---
    block1, block2 = find_digit_blocks(input_nums, target)
    
    # Check if exactly two blocks were found as expected from examples
    # If not, the input format deviates; return zeros or handle error
    # Based on find_digit_blocks logic, if not 2 blocks, it returns [],[] or [block1],[]
    # The padding logic below will handle these cases by padding mostly zeros.

    # --- Step 3 & 4: Compare Lengths and Rearrange ---
    output_prefix = []
    if len(block1) > len(block2):
        # If B1 is strictly longer, the order is B2, 0, B1
        output_prefix.extend(block2)
        output_prefix.append(0)
        output_prefix.extend(block1)
    else:
        # Otherwise (B1 is shorter or equal), the order is B1, 0, B2
        output_prefix.extend(block1)
        output_prefix.append(0)
        output_prefix.extend(block2)

    # --- Step 5: Pad with Zeros ---
    # Create the final output list starting with the rearranged prefix
    output_nums = output_prefix[:] # Make a copy

    # Calculate how many zeros are needed for padding
    padding_needed = output_size - len(output_nums)
    
    if padding_needed > 0:
        # Append the required number of zeros
        output_nums.extend([0] * padding_needed)
    elif padding_needed < 0:
        # If the combined blocks + zero exceeded the output size (should not happen with valid inputs)
        # Truncate the list to the correct size
        output_nums = output_nums[:output_size]

    # --- Step 6: Return the Result ---
    return output_nums