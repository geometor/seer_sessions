import math
import collections

"""
Transformation Rule:

The transformation operates on a sequence of 12 single-digit integers.
It searches for the first occurrence of a specific pattern: a non-zero digit (anchor), 
followed immediately by one or more zeros, followed immediately by a contiguous block 
of identical non-zero digits (moving block).

If this pattern is found, the moving block shifts leftwards, overwriting some of the 
preceding zeros. The number of positions shifted (`shift_amount`) is the minimum of 
the count of preceding zeros and the length of the moving block. The zeros that were 
overwritten by the shift are moved to the end of the sequence.

If the pattern is not found, or if the calculated `shift_amount` is zero (meaning 
there are no zeros between the anchor and the block, or the block has length zero, 
which shouldn't happen with non-zero blocks), the sequence remains unchanged.
"""

def parse_input(input_str: str) -> list[int]:
    """Converts the space-separated string input into a list of integers."""
    return [int(digit) for digit in input_str.split()]

def format_output(grid: list[int]) -> str:
    """Converts the list of integers back into a space-separated string."""
    return " ".join(map(str, grid))

def find_pattern(grid: list[int]):
    """
    Finds the first occurrence of the anchor -> zeros -> block pattern.

    Returns:
        A dictionary containing pattern details 
        {'anchor_index', 'zero_count', 'block_start', 'block_length', 'block_value'} 
        if found, otherwise None.
    """
    n = len(grid)
    i = 0
    while i < n:
        # 1. Find a potential anchor (non-zero digit)
        if grid[i] != 0:
            anchor_index = i
            
            # 2. Look for preceding zeros immediately after the anchor
            j = i + 1
            if j < n and grid[j] == 0:
                zero_start = j
                while j < n and grid[j] == 0:
                    j += 1
                zero_count = j - zero_start

                # 3. Look for a block of identical non-zero digits immediately after the zeros
                if j < n and grid[j] != 0:
                    block_start = j
                    block_value = grid[j]
                    k = j + 1
                    while k < n and grid[k] == block_value:
                        k += 1
                    block_length = k - block_start
                    
                    # Pattern found!
                    return {
                        "anchor_index": anchor_index,
                        "zero_count": zero_count,
                        "block_start": block_start,
                        "block_length": block_length,
                        "block_value": block_value,
                    }
                else:
                    # Zeros found, but no block afterwards. Continue search from end of zeros.
                    i = j 
            else:
                # Anchor found, but no zeros immediately after. Continue search from next position.
                i += 1
        else:
            # Current element is zero, continue search from next position.
            i += 1
            
    # Pattern not found after scanning the whole grid
    return None

def transform(input_str: str) -> str:
    """
    Applies the transformation rule to the input string.
    """
    # Parse the input string into a list of integers
    grid = parse_input(input_str)
    n = len(grid)

    # Find the first occurrence of the anchor -> zeros -> block pattern
    pattern_info = find_pattern(grid)

    # If the pattern is not found, return the original grid formatted as a string
    if pattern_info is None:
        return format_output(grid)

    # Extract pattern details
    zero_count = pattern_info["zero_count"]
    block_start = pattern_info["block_start"]
    block_length = pattern_info["block_length"]
    block_value = pattern_info["block_value"]

    # Calculate the shift amount
    shift_amount = min(zero_count, block_length)

    # If shift_amount is 0, no transformation needed
    if shift_amount == 0:
         return format_output(grid)

    # Construct the new grid
    new_grid = []
    
    # Part before the removed zeros
    # The zeros to be removed start at index block_start - shift_amount
    new_grid.extend(grid[0 : block_start - shift_amount])
    
    # The moved block
    new_grid.extend([block_value] * block_length)
    
    # The part after the original block
    new_grid.extend(grid[block_start + block_length : n])
    
    # The zeros moved to the end
    new_grid.extend([0] * shift_amount)
    
    # Ensure the output grid has the correct length (should be handled by logic above)
    # assert len(new_grid) == n, f"Length mismatch: expected {n}, got {len(new_grid)}"

    # Format the final list back into a space-separated string for the output
    return format_output(new_grid)
