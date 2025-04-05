"""
Shift a trailing sub-sequence (starting from the first non-zero digit) left by 3 positions within a fixed-length digit list.

1. Examine the input list of 12 digits to find the index of the first digit that is not zero. Let this index be `start_index`.
2. If no non-zero digit exists in the input list (i.e., all digits are 0), the output list is identical to the input list.
3. If a non-zero digit is found at `start_index`:
    a. Define the `active_block` as the sub-list containing all digits from `start_index` to the end of the input list.
    b. Calculate the target starting position for this block in the output list: `new_start_index = start_index - 3`.
    c. Construct the output list:
        i. Begin with `new_start_index` zeros.
        ii. Append the `active_block`.
        iii. Append additional zeros to the end until the total length of the output list reaches 12.
4. Return the constructed output list.
"""

# No specific imports needed for basic list operations

def find_first_non_zero_index(digit_list):
    """Finds the index of the first non-zero digit in a list."""
    for index, digit in enumerate(digit_list):
        if digit != 0:
            return index
    return -1 # Return -1 if no non-zero digit is found

def transform(input_list):
    """
    Applies the transformation rule to the input list of digits.
    """
    # Define the fixed length of the sequence
    list_length = 12

    # 1. Find the index of the first non-zero digit.
    start_index = find_first_non_zero_index(input_list)

    # 2. Handle the case where all digits are zero.
    if start_index == -1:
        return list(input_list) # Return a copy of the input list

    # 3. If a non-zero digit is found:
    # a. Extract the active block (from the first non-zero digit to the end).
    active_block = input_list[start_index:]

    # b. Calculate the new starting position for the block.
    #    Ensure the new start index isn't negative, though based on examples
    #    it seems the first non-zero will always be at index >= 3 if present.
    #    If it could be less than 3, we might need clarification.
    #    For now, assume it's always >= 3 if a non-zero exists.
    new_start_index = start_index - 3
    # Ensure non-negative index, though likely unnecessary based on examples
    # new_start_index = max(0, new_start_index)

    # c. Construct the output list.
    # Initialize the output list
    output_list = []

    # i. Add leading zeros.
    output_list.extend([0] * new_start_index)

    # ii. Append the active block.
    output_list.extend(active_block)

    # iii. Append trailing zeros to reach the fixed length.
    trailing_zeros_count = list_length - len(output_list)
    if trailing_zeros_count > 0:
        output_list.extend([0] * trailing_zeros_count)
    # Handle potential overshoot if active_block makes list longer than 12
    # after shifting (unlikely given problem constraints but good practice)
    elif trailing_zeros_count < 0:
         output_list = output_list[:list_length]


    # 4. Return the constructed output list.
    return output_list
