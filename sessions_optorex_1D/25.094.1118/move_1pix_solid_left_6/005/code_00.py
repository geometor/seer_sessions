import math # Included standard math library, although not used in this specific solution
import numpy as np # Included standard numpy library, although not used in this specific solution

"""
Transforms a sequence of 12 digits by finding a single contiguous block of 
identical non-zero digits and shifting this entire block one position to the left. 
Positions outside the shifted block are filled with zeros.

1.  Parse Input: Convert the input space-separated string of 12 digits into a 
    list of integers.
2.  Locate Block: Identify the starting index (`start_idx`) and ending index 
    (`end_idx`) of the single contiguous sequence of identical non-zero digits. 
    If no non-zero digits exist, the result is a sequence of 12 zeros.
3.  Initialize Output: Create a new list of 12 elements, initially all set to 
    zero.
4.  Calculate New Position: Determine the new starting index for the block in 
    the output as `new_start_idx = start_idx - 1`.
5.  Extract Block: Get the sub-sequence of non-zero digits from the input list 
    using `start_idx` and `end_idx`.
6.  Place Block in Output: Copy the extracted block into the output list, 
    starting at `new_start_idx`.
7.  Format Output: Convert the resulting output list back into a 
    space-separated string of digits.
"""

def parse_input(input_str: str) -> list[int]:
    """Converts a space-separated string of digits into a list of integers."""
    # Handles potential errors if input is not digits or not space-separated
    try:
        return [int(digit) for digit in input_str.split()]
    except ValueError:
        # Return an empty list or handle error as appropriate if parsing fails
        # For this problem, assuming valid input format based on examples.
        print(f"Warning: Could not parse input string: {input_str}")
        return [] 

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
    Input is expected as a space-separated string.
    Output is returned as a space-separated string.
    """
    
    # 1. Parse Input string into a list of integers
    input_list = parse_input(input_str)
    
    # Basic validation - check if input parsing was successful and length is 12
    if not input_list or len(input_list) != 12:
        # Handle error case - perhaps return input or an error indicator
        # Based on problem, assume input is always valid 12 digits.
        # If not, returning zeros might be a safe default.
        return "0 0 0 0 0 0 0 0 0 0 0 0" 
        
    n = len(input_list) # Should be 12

    # 2. Locate the contiguous block of non-zero digits
    start_index, end_index = find_nonzero_block(input_list)

    # 3. Initialize Output list with zeros
    output_list = [0] * n

    # Proceed only if a non-zero block was found
    if start_index != -1:
        # 4. Calculate the new starting position (shifted one to the left)
        # Based on examples, start_index is always > 0, so new_start_index >= 0.
        new_start_index = start_index - 1

        # 5. Extract the block of non-zero digits from the input list
        # Slicing is [start:end+1] to include the end_index element
        block = input_list[start_index : end_index + 1]
        block_len = len(block) # Or calculate as end_index - start_index + 1

        # 6. Place the extracted block into the output list at the new position
        # Check boundaries just in case, though examples suggest it always fits.
        if new_start_index >= 0:
             # Iterate through the block and place elements
             for i in range(block_len):
                 # Calculate the target index in the output list
                 output_index = new_start_index + i
                 # Ensure we don't write out of bounds (shouldn't happen with left shift)
                 if output_index < n:
                     output_list[output_index] = block[i]
                 # else: part of the block would shift off the end - ignore based on examples

    # 7. Format the output list back into a space-separated string
    output_str = format_output(output_list)

    return output_str