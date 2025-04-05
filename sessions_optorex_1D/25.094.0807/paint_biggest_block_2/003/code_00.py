import numpy as np
import math # Not strictly needed for this logic, but available
import re   # Not strictly needed for this logic, but available

"""
Transforms a sequence of digits based on the following rules:
1. Receive the input data, which represents a sequence of digits.
2. Convert the input data into a standard Python list of integers. Handle potential input types like strings, lists, or NumPy arrays appropriately.
3. Identify all contiguous sub-sequences (blocks) within the integer list that are composed of identical, non-zero digits. For each block, record its starting index, ending index, and length.
4. If no non-zero blocks are found, proceed directly to step 8 using the original integer list.
5. Find the maximum length among all identified blocks.
6. Select the target block: Choose the block that has this maximum length. If multiple blocks share the maximum length, select the one with the smallest starting index (the leftmost one).
7. Create a new list of integers, initially as a copy of the standardized input list. Iterate from the starting index to the ending index (inclusive) of the selected target block in this new list, changing each digit within this range to `1`.
8. Format the resulting list of integers (either the modified list from step 7 or the original list if no blocks were found/modified) into a space-separated string of digits for the final output.
"""

def find_contiguous_blocks(numbers):
    """
    Identifies contiguous blocks of identical non-zero digits in a list of numbers.

    Args:
        numbers: A list of integers.

    Returns:
        A list of dictionaries, where each dictionary represents a block
        and contains 'start', 'end', 'length', and 'value' keys.
        Returns an empty list if no non-zero blocks are found.
    """
    blocks = []
    if not numbers:
        return blocks

    start_index = -1
    current_digit = -1 # Use a value that won't match 0-9 initially
    count = 0

    for i, num in enumerate(numbers):
        # Case 1: Start of a new non-zero block or continuation of the current one
        if num != 0:
            if num == current_digit:
                count += 1
            else:
                # Finalize the previous block if it existed and was non-zero
                if current_digit != -1 and current_digit != 0 and count > 0:
                    blocks.append({'start': start_index, 'end': i - 1, 'length': count, 'value': current_digit})
                
                # Start a new potential block
                start_index = i
                current_digit = num
                count = 1
        # Case 2: Encountered a zero or end of a block
        else:
            # Finalize the previous block if it existed and was non-zero
            if current_digit != -1 and current_digit != 0 and count > 0:
                 blocks.append({'start': start_index, 'end': i - 1, 'length': count, 'value': current_digit})

            # Reset tracking as we encountered a zero
            start_index = -1
            current_digit = 0 # Explicitly track seeing a zero, though reset is key
            count = 0

    # Check for a block ending at the very end of the sequence
    if current_digit != -1 and current_digit != 0 and count > 0:
        blocks.append({'start': start_index, 'end': len(numbers) - 1, 'length': count, 'value': current_digit})

    return blocks


def transform(input_data) -> str:
    """
    Applies the transformation rule to the input data.
    """
    # --- 1 & 2. Standardize Input ---
    # Convert input (potentially numpy array, string, or list) to a list of integers.
    if isinstance(input_data, np.ndarray):
        # Assuming 1D array or flatten if multi-dimensional might be needed
        numbers = input_data.flatten().tolist()
    elif isinstance(input_data, str):
        # Handle space-separated string input
        try:
            numbers = [int(digit) for digit in input_data.split()]
        except ValueError:
             # Handle case where split elements are not digits, though unlikely based on examples
            raise TypeError("Input string contains non-integer values.")
    elif isinstance(input_data, list):
        # Assume list contains numbers (int or float convertible to int)
        try:
            numbers = [int(x) for x in input_data]
        except (ValueError, TypeError):
             raise TypeError("Input list contains non-integer values.")
    else:
        raise TypeError(f"Unsupported input type: {type(input_data)}")

    # Initialize the output list as a copy of the input list
    output_numbers = list(numbers)

    # --- 3. Identify Blocks ---
    blocks = find_contiguous_blocks(numbers)

    # --- 4. Handle No Blocks Case ---
    if not blocks:
        # If no non-zero blocks, format the original list and return
        return " ".join(map(str, numbers))

    # --- 5. Find Max Length ---
    max_length = 0
    for block in blocks:
        if block['length'] > max_length:
            max_length = block['length']

    # --- 6. Select Target Block ---
    target_block = None
    for block in blocks:
        if block['length'] == max_length:
            # The first block found with max_length is the leftmost one
            target_block = block
            break # Stop searching once the first (leftmost) longest block is found

    # --- 7. Modify Block ---
    # Only modify if a target block was actually found (handles edge case of only zeros)
    if target_block:
        start = target_block['start']
        end = target_block['end']
        # Iterate through the indices of the target block in the output list
        for i in range(start, end + 1):
            output_numbers[i] = 1 # Change the value to 1

    # --- 8. Format Output ---
    # Convert the potentially modified list back to a space-separated string
    output_str = " ".join(map(str, output_numbers))

    return output_str