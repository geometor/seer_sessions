import math
# Potential future imports if needed, though basic list operations suffice for now.
# import numpy as np 

"""
Transforms an input sequence of digits according to the following rule:
1. Identifies the two contiguous blocks of identical non-zero digits present in the input sequence.
2. Counts the total number of zero digits in the input sequence.
3. Orders the two identified non-zero blocks based on their length: the shorter block comes first. 
   If the blocks have equal lengths, their original order (as found in the input) is preserved.
4. Constructs the output sequence by concatenating:
   - The first block (according to the ordering rule).
   - A single zero digit (if any zeros were present in the input).
   - The second block (according to the ordering rule).
   - All the remaining zero digits from the input appended at the end.
"""

def find_non_zero_blocks(data):
    """
    Finds contiguous blocks of identical non-zero digits in a list of integers.

    Args:
        data: A list of integers.

    Returns:
        A list containing the two identified blocks, each represented as a list of integers.
        Returns an empty list if fewer than two blocks are found.
    """
    blocks = []
    current_block = []
    in_block = False
    last_digit = -1 # Sentinel value different from 0-9

    for digit in data:
        if digit != 0:
            # Handle start of a block or continuation of the current block
            if not in_block: 
                # Start of a new block
                in_block = True
                current_block = [digit]
                last_digit = digit
            elif digit == last_digit:
                # Continue current block
                current_block.append(digit)
            else:
                # Encountered a *different* non-zero digit immediately after another.
                # This signifies the end of the previous block *and* the start of a new one.
                # According to observed examples, blocks are separated by zeros,
                # so this case implies either the end of the first block (if adjacent to a zero later)
                # or potentially an unexpected input pattern if no zeros separate different non-zero digits.
                # Let's refine the logic: a block ends when a 0 is seen, or a *different* non-zero digit is seen,
                # or the end of the list is reached.
                if current_block: # Store the completed block
                     blocks.append(list(current_block)) # Use list() for a copy
                     if len(blocks) == 2: break # Optimization
                # Start the new block
                current_block = [digit]
                last_digit = digit
                in_block = True # Ensure we are marked as in_block

        elif digit == 0:
            # A zero marks the end of any active non-zero block
            if in_block:
                blocks.append(list(current_block)) # Use list() for a copy
                if len(blocks) == 2: # Optimization: Stop once two blocks are found
                     break
                current_block = []
                in_block = False
            last_digit = 0 # Reset last digit tracker (though not strictly needed for block logic)

    # Handle the case where the last block extends to the end of the list
    if in_block and current_block and len(blocks) < 2:
         blocks.append(list(current_block)) # Use list() for a copy

    # We expect exactly two blocks based on the problem description and examples
    if len(blocks) == 2:
        return blocks
    else:
        # Handle potential edge cases or malformed input if necessary.
        # Returning the found blocks allows the caller to decide how to handle errors.
        # print(f"Warning/Error: Found {len(blocks)} non-zero blocks, expected 2 in data: {data}")
        # For robustness based on examples, perhaps return only first two if more are found?
        # Or raise an error? Let's stick to returning what's found for now.
        return blocks


def transform(input_data):
    """
    Applies the transformation rule to the input list/array of digits.

    Args:
        input_data: A list or NumPy array of integers representing the input sequence.

    Returns:
        A list of integers representing the transformed sequence. Returns an empty list
        or raises an error if the input doesn't contain exactly two non-zero blocks
        as expected by the observed pattern.
    """
    
    # Ensure input is a standard list for consistency
    # (Handles cases where input might be a NumPy array)
    input_list = list(input_data) 

    # Count the total number of zeros
    zero_count = input_list.count(0)

    # Find the two non-zero blocks using the helper function
    blocks = find_non_zero_blocks(input_list)

    # --- Validation ---
    # Ensure exactly two blocks were found, as expected from all examples
    if len(blocks) != 2:
        # This indicates an input format inconsistent with the observed examples.
        # Depending on requirements, could raise an error, return input, or return empty.
        # Returning empty list for now to signal failure based on pattern mismatch.
        print(f"Error: Expected 2 non-zero blocks, found {len(blocks)} in input: {input_list}")
        # raise ValueError(f"Input data must contain exactly two non-zero blocks. Found {len(blocks)}.")
        return [] 
    # --- End Validation ---

    # Assign the found blocks
    block1 = blocks[0]
    block2 = blocks[1]

    # Compare lengths of the blocks to determine the output order
    if len(block1) <= len(block2):
        # If block1 is shorter or equal length, it comes first
        first_block = block1
        second_block = block2
    else:
        # If block1 is longer, block2 comes first
        first_block = block2
        second_block = block1

    # --- Construct the output list ---
    # Start with the first ordered block
    output_list = list(first_block) # Ensure it's a list copy

    # Add the single zero separator (only if there were zeros in the input)
    if zero_count > 0:
        output_list.append(0)

    # Add the second ordered block
    output_list.extend(second_block)

    # Add the remaining zeros to the end
    # Calculate how many zeros are left after using one as a separator
    remaining_zeros = max(0, zero_count - 1) 
    output_list.extend([0] * remaining_zeros)
    # --- End Construction ---

    # Return the transformed list
    return output_list