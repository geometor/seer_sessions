import re

"""
Transforms a sequence of 12 digits, provided as a space-separated string,
by identifying a single contiguous block of identical non-zero digits
and shifting this block to the right by a distance equal to its own length.
The remaining positions are filled with zeros, and the output is returned
as a space-separated string.
"""

def find_non_zero_block(digit_sequence):
    """
    Finds the start index, digit value, and length of the first contiguous
    block of identical non-zero digits in a sequence.

    Args:
        digit_sequence: A string containing only digits (e.g., "000111000").

    Returns:
        A tuple (start_index, digit_value, block_length) if a block is found.
        Returns None if the sequence contains only zeros or no valid block.
    """
    start_index = -1
    digit_value = '0'
    block_length = 0

    # Find the start of the first non-zero block
    for i, char in enumerate(digit_sequence):
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
    for i in range(start_index, len(digit_sequence)):
        if digit_sequence[i] == digit_value:
            block_length += 1
        else:
            # Stop counting when a different digit (or zero) is encountered
            break

    # Basic validation: if block_length is 0 after finding a start, something is wrong
    # but the logic above should prevent this unless the sequence is empty or malformed.
    if block_length == 0:
         return None # Should not happen with valid non-zero start found

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
    default_output = " ".join(['0'] * sequence_length)

    # --- Step 1 & 2: Preprocess Input ---
    # Ensure input is treated as a string
    input_string = str(input_grid)
    # Remove spaces to get the pure digit sequence
    cleaned_sequence = "".join(input_string.split())

    # Validate the length of the cleaned sequence
    if len(cleaned_sequence) != sequence_length:
        # Handle invalid input length - return default or raise error
        # For this task, returning default zero sequence seems reasonable
        # print(f"Warning: Input sequence length is not {sequence_length} after cleaning: '{cleaned_sequence}'")
        return default_output
    # Validate if sequence contains only digits 0-9
    if not cleaned_sequence.isdigit():
        # print(f"Warning: Input sequence contains non-digit characters after cleaning: '{cleaned_sequence}'")
        return default_output


    # --- Step 3: Initialize Output ---
    # Create an output list initialized with zeros
    output_list = ['0'] * sequence_length

    # --- Step 4 & 5: Find the Non-Zero Block ---
    # Use the helper function to find the block details
    block_info = find_non_zero_block(cleaned_sequence)

    # --- Step 6 & 7: Calculate Shift and Place Block (if found) ---
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

    # --- Step 8: Format Output ---
    # Join the characters in the output list using a single space separator
    output_grid_str = " ".join(output_list)

    # --- Step 9: Return Result ---
    return output_grid_str