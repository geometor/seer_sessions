"""
Transforms an input NumPy array representing a sequence of 12 digits.
The transformation identifies contiguous blocks of identical digits. It then looks for the first occurring pattern where the first block and the last block of a specific digit are separated only by blocks of different digits. If found, one digit is conceptually moved from the end of the first block to the end of the last block by adjusting their lengths. The sequence is then reconstructed from the modified block lengths and returned as a NumPy array.
"""

import numpy as np
from typing import List, Tuple

# Helper function to identify blocks of consecutive identical digits
def _identify_blocks(digits: List[int]) -> List[Tuple[int, int]]:
    """
    Identifies contiguous blocks of identical digits in a list.
    Returns a list of tuples, where each tuple is (digit, length).
    Example: [0, 0, 5, 5, 5, 0] -> [(0, 2), (5, 3), (0, 1)]
    """
    if not digits:
        return []

    blocks = []
    # Initialize with the first element if list is not empty
    current_digit = digits[0]
    current_length = 0
    
    for digit in digits:
        if digit == current_digit:
            current_length += 1
        else:
            # Append the completed block if its length is positive
            if current_length > 0:
                 blocks.append((current_digit, current_length))
            # Start the new block
            current_digit = digit
            current_length = 1
            
    # Append the very last block after the loop finishes
    if current_length > 0:
        blocks.append((current_digit, current_length))
        
    return blocks

# Helper function to reconstruct the sequence list from blocks
def _reconstruct_sequence_list(blocks: List[Tuple[int, int]]) -> List[int]:
    """
    Reconstructs the list of digits from a list of blocks.
    Omits blocks with zero length.
    Example: [(0, 2), (5, 3), (0, 1)] -> [0, 0, 5, 5, 5, 0]
    Example: [(0, 0), (5, 3), (0, 1)] -> [5, 5, 5, 0]
    """
    output_digits = []
    for digit, length in blocks:
        # Only add blocks with positive length
        if length > 0:
            output_digits.extend([digit] * length)
    return output_digits

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the element transfer rule to the input NumPy array.
    """
    # 1. Flatten the input array to a 1D list of digits
    #    This handles both 1D and potential 1xN 2D arrays correctly.
    if input_grid.size == 0:
        return np.array([]) # Handle empty input gracefully
    digits = input_grid.flatten().tolist()
    original_dtype = input_grid.dtype # Preserve original data type

    # 2. Identify contiguous blocks of identical digits
    blocks = _identify_blocks(digits)
    if not blocks: 
        # Should not happen if input wasn't empty, but handle defensively
        return np.array(digits, dtype=original_dtype) 

    # 3. Find the transfer pattern
    #    Iterate through unique digits present in the blocks.
    #    Using dict.fromkeys preserves the order of appearance, ensuring we find
    #    the *first* pattern according to the order digits appear in the sequence.
    unique_digits_ordered = list(dict.fromkeys(d[0] for d in blocks))
    
    transformed = False
    new_blocks = list(blocks) # Work on a mutable copy

    for digit_to_check in unique_digits_ordered:
        if transformed: # Optimization: Stop after the first successful transformation
            break

        # 4. Find indices of the first and last blocks containing this digit
        first_idx = -1
        last_idx = -1
        indices = [i for i, block in enumerate(new_blocks) if block[0] == digit_to_check]

        if len(indices) >= 2: # Need at least two blocks of the same digit
            first_idx = indices[0]
            last_idx = indices[-1]

        # 5. Check if blocks are distinct and separated only by other digits
        if first_idx != -1: # This check implicitly covers first_idx < last_idx because indices are sorted
            is_separated_correctly = True
            # Check all blocks *between* the first and last candidates
            for i in range(first_idx + 1, last_idx):
                if new_blocks[i][0] == digit_to_check:
                    # Found a block of the same digit in between - invalid pattern
                    is_separated_correctly = False
                    break 

            # 6. If conditions met, perform the transfer
            if is_separated_correctly:
                # Ensure the first block actually has elements to move
                if new_blocks[first_idx][1] > 0:
                    # a. Decrease length of the first block
                    first_block_val, first_block_len = new_blocks[first_idx]
                    new_blocks[first_idx] = (first_block_val, first_block_len - 1)

                    # b. Increase length of the last block
                    last_block_val, last_block_len = new_blocks[last_idx]
                    new_blocks[last_idx] = (last_block_val, last_block_len + 1)

                    # c. Mark as transformed and stop searching for other patterns
                    transformed = True
                    # Note: Block removal (if length becomes 0) happens during reconstruction

    # 7. Reconstruct the sequence list from potentially modified blocks
    #    The helper function handles skipping blocks with length 0.
    output_list = _reconstruct_sequence_list(new_blocks)

    # 8. Convert the result list back to a NumPy array with original dtype
    output_grid = np.array(output_list, dtype=original_dtype)

    return output_grid