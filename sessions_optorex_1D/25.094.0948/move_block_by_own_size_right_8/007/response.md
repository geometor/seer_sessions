```python
import re # Although not strictly needed for the final implementation, keeping it as it was included before.

"""
Transforms a sequence of 12 digits, provided as a space-separated string,
by identifying a single contiguous block of identical non-zero digits
and shifting this block to the right by a distance equal to its own length.
The remaining positions are filled with zeros, and the output is returned
as a space-separated string.
"""

def find_non_zero_block(digit_list):
    """
    Finds the start index, digit value, and length of the first contiguous
    block of identical non-zero digits in a list of digit characters.

    Args:
        digit_list: A list of strings, where each string is a single digit ('0'-'9').

    Returns:
        A tuple (start_index, digit_value, block_length) if a block is found.
        Returns None if the sequence contains only zeros or no valid block.
    """
    start_index = -1
    digit_value = '0'
    block_length = 0
    sequence_length = len(digit_list)

    # Find the start of the first non-zero block
    for i, char in enumerate(digit_list):
        # Check if the character is a non-zero digit
        if char != '0' and '1' <= char <= '9':
            start_index = i
            digit_value = char
            break

    # If no non-zero digit was found (e.g., all zeros), return None
    if start_index == -1:
        return None

    # Count the length of the contiguous block starting from start_index
    # Ensure we only count contiguous identical non-zero digits
    for i in range(start_index, sequence_length):
        if digit_list[i] == digit_value:
            block_length += 1
        else:
            # Stop counting when a different digit (or zero) is encountered
            break

    # If block_length is 0 after finding a start, something is wrong (should not happen here)
    if block_length == 0:
         return None

    return start_index, digit_value, block_length

def transform(input_grid):
    """
    Applies the transformation rule to the input grid string.

    Args:
        input_grid: A string representing the sequence of 12 digits,
                    separated by spaces (e.g., "0 0 0 1 1 1 0 0 0 0 0 0").

    Returns:
        A string representing the transformed sequence, with digits
        separated by spaces (e.g., "0 0 0 0 0 0 1 1 1 0 0 0").
        Returns a default zero string if input is invalid or has no block.
    """
    # Define the expected length of the digit sequence
    sequence_length = 12
    default_output_list = ['0'] * sequence_length

    # --- Step 1: Parse Input ---
    # Ensure input is treated as a string and split into a list of characters
    try:
        input_list = str(input_grid).split(' ')
        # Basic validation: check length and if all elements are single digits
        if len(input_list) != sequence_length or not all(s.isdigit() and len(s) == 1 for s in input_list):
             # print(f"Warning: Invalid input format or length: {input_grid}")
             return " ".join(default_output_list)
    except Exception as e: # Catch potential errors during split or processing
        # print(f"Error processing input: {e}")
        return " ".join(default_output_list)


    # --- Step 2: Initialize Output ---
    # Create an output list initialized with zeros
    output_list = ['0'] * sequence_length

    # --- Step 3: Find the Non-Zero Block ---
    # Use the helper function to find the block details in the parsed list
    block_info = find_non_zero_block(input_list)

    # --- Step 4: Calculate Shift and Place Block (if found) ---
    # Proceed only if a valid block was found
    if block_info:
        start_index, digit_value, block_length = block_info

        # Calculate the new starting index for the block in the output
        new_start_index = start_index + block_length

        # Place the block into the output list at the calculated new position
        # Iterate for the length of the block
        for i in range(block_length):
            # Calculate the target index in the output list
            target_index = new_start_index + i
            # IMPORTANT: Check if the target index is within the bounds of the output list
            if target_index < sequence_length:
                output_list[target_index] = digit_value
            # else: block goes partially or fully out of bounds, ignore the out-of-bounds part

    # --- Step 5: Format Output ---
    # Join the characters in the output list using a single space separator
    output_grid_str = " ".join(output_list)

    # --- Step 6: Return Result ---
    return output_grid_str
```