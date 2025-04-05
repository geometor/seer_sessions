import math

def find_first_non_zero_index(data_list):
    """Finds the index of the first non-zero element."""
    for i, val in enumerate(data_list):
        if val != 0:
            return i
    return -1 # Return -1 if all are zeros

def find_last_non_zero_index(data_list):
    """Finds the index of the last non-zero element."""
    for i in range(len(data_list) - 1, -1, -1):
        if data_list[i] != 0:
            return i
    return -1 # Return -1 if all are zeros

def transform(input_str: str) -> str:
    """
    Reverses the sub-sequence of digits located between the first and last
    non-zero digits in the input sequence, leaving any leading and trailing
    zeros in their original positions.

    1.  Parses the input string into a list of integers.
    2.  Finds the index of the first non-zero digit (`start_index`).
    3.  Finds the index of the last non-zero digit (`end_index`).
    4.  If no non-zero digits are found (all zeros), returns the original string.
    5.  Otherwise, extracts the prefix (leading zeros before `start_index`).
    6.  Extracts the middle segment (from `start_index` to `end_index`, inclusive).
    7.  Extracts the suffix (trailing zeros after `end_index`).
    8.  Reverses the middle segment.
    9.  Concatenates the prefix, reversed middle segment, and suffix.
    10. Formats the result back into a space-separated string.
    """
    # 1. Parse the input string into a list of integers.
    input_list = [int(x) for x in input_str.split()]

    # 2. Find the index of the first non-zero digit.
    start_index = find_first_non_zero_index(input_list)

    # 4. If no non-zero digits are found (all zeros), return the original string.
    if start_index == -1:
        return input_str

    # 3. Find the index of the last non-zero digit.
    end_index = find_last_non_zero_index(input_list)

    # 5. Extract the prefix (leading zeros before start_index).
    prefix = input_list[:start_index]

    # 6. Extract the middle segment (from start_index to end_index, inclusive).
    middle = input_list[start_index : end_index + 1]

    # 7. Extract the suffix (trailing zeros after end_index).
    suffix = input_list[end_index + 1:]

    # 8. Reverse the middle segment.
    reversed_middle = middle[::-1]

    # 9. Concatenate the prefix, reversed middle segment, and suffix.
    output_list = prefix + reversed_middle + suffix

    # 10. Format the result back into a space-separated string.
    output_str = " ".join(map(str, output_list))

    return output_str
