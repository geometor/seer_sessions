```python
"""
Transform a sequence of 12 digits based on the following rules:

1.  **Receive Input:** Start with the input string containing 12 space-separated digits.
2.  **Parse Input:** Convert the input string into a list of 12 integer digits. Let this be `digit_list`.
3.  **Find Start:** Iterate through `digit_list` from the beginning (index 0) to find the index of the first digit that is not 0. Let this index be `start_index`.
4.  **Handle All Zeros:** If no non-zero digit is found (`start_index` remains undefined or is marked as -1), the final result list is identical to the initial `digit_list`. Proceed to Step 8.
5.  **Extract Block:** If a non-zero digit is found at `start_index`, extract the `active_block`, which is the sub-list containing all elements of `digit_list` from `start_index` to the end.
6.  **Calculate New Position:** Determine the target starting index for the `active_block` in the output: `new_start_index = start_index - 3`.
7.  **Construct Output List:** Create a new list (`result_list`) of 12 digits as follows:
    a.  Add `new_start_index` number of zeros to the beginning of `result_list`.
    b.  Append all digits from the `active_block` to `result_list`.
    c.  Append trailing zeros to `result_list` until its total length reaches 12.
8.  **Format Output:** Convert the `result_list` (either from Step 4 or Step 7) back into a string where each digit is separated by a space.
9.  **Return Output:** Return the final formatted string.
"""

# No external libraries needed

def find_first_non_zero_index(sequence):
    """
    Finds the index of the first non-zero element in a sequence.

    Args:
        sequence: A list of numbers.

    Returns:
        The index of the first non-zero element, or -1 if all elements are zero.
    """
    for index, element in enumerate(sequence):
        if element != 0:
            return index
    return -1

def transform(input_str):
    """
    Applies the transformation rule to the input string of digits.

    Args:
        input_str: A string containing 12 space-separated digits.

    Returns:
        A string containing the transformed 12 space-separated digits.
    """
    # Define constants
    sequence_length = 12
    shift_amount = 3

    # 2. Parse Input: Convert the input string into a list of integers.
    try:
        digit_list = [int(d) for d in input_str.split()]
        # Basic validation for length
        if len(digit_list) != sequence_length:
             # Handle error or assume correct length based on problem spec
             # For now, let it proceed, but this could be an error point
             pass
    except ValueError:
        # Handle potential non-integer input if necessary
        print(f"Error: Input string '{input_str}' contains non-integer characters.")
        return "" # Or raise an exception

    # 3. Find Start: Find the index of the first non-zero digit.
    start_index = find_first_non_zero_index(digit_list)

    # Initialize the result list
    result_list = []

    # 4. Handle All Zeros: If no non-zero digit is found, use the original list.
    if start_index == -1:
        result_list = list(digit_list) # Use a copy
    else:
        # 5. Extract Block: Get the sub-list from start_index onwards.
        active_block = digit_list[start_index:]

        # 6. Calculate New Position: Determine the target starting index.
        new_start_index = start_index - shift_amount
        # Ensure the index is not negative (though examples suggest it won't be)
        new_start_index = max(0, new_start_index)

        # 7. Construct Output List:
        # a. Add leading zeros.
        result_list.extend([0] * new_start_index)

        # b. Append the active block.
        result_list.extend(active_block)

        # c. Append trailing zeros until the total length reaches sequence_length.
        trailing_zeros_count = sequence_length - len(result_list)
        if trailing_zeros_count > 0:
            result_list.extend([0] * trailing_zeros_count)
        # Truncate if somehow the shifted block makes it too long (unlikely given constraints)
        elif trailing_zeros_count < 0:
            result_list = result_list[:sequence_length]

    # 8. Format Output: Convert the result list back into a space-separated string.
    output_str = " ".join(map(str, result_list))

    # 9. Return Output: Return the final formatted string.
    return output_str
```