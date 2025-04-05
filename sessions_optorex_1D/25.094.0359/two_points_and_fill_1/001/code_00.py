import math

"""
Identifies the single non-zero digit ('fill_value') present exactly twice in the input list. 
Fills the elements between the first and second occurrences of the 'fill_value' with the 'fill_value' itself. 
Elements outside this range remain unchanged.
"""

def find_first(lst, value):
    """Helper function to find the first index of a value in a list."""
    for i, x in enumerate(lst):
        if x == value:
            return i
    return -1 # Should not happen based on problem description

def find_last(lst, value):
    """Helper function to find the last index of a value in a list."""
    for i in range(len(lst) - 1, -1, -1):
        if lst[i] == value:
            return i
    return -1 # Should not happen based on problem description

def transform(input_str: str) -> str:
    """
    Transforms the input string list by filling zeros between two occurrences 
    of a non-zero digit with that digit.
    """
    # 1. Parse the input string into a list of integers.
    input_list = [int(x) for x in input_str.split()]

    # 2. Identify the non-zero integer (fill_value).
    fill_value = 0
    for x in input_list:
        if x != 0:
            fill_value = x
            break # Found the first non-zero, which is the fill value

    # Check if a fill_value was found (handles edge case of all zeros, though not expected)
    if fill_value == 0:
        return input_str # No non-zero value, return original string

    # 3. Find the index of the first occurrence (idx1).
    idx1 = find_first(input_list, fill_value)

    # 4. Find the index of the second occurrence (idx2).
    # We search from idx1 + 1 onwards to ensure we find the *second* occurrence.
    # A simpler way is to find the *last* occurrence, as there are only two.
    idx2 = find_last(input_list, fill_value)

    # 5. Create a copy of the input list to serve as the initial output list.
    output_list = list(input_list)

    # 6. Iterate through the indices i from idx1 + 1 up to (but not including) idx2.
    # 7. For each index i in this range, set the element at index i in the output list to the fill_value.
    if idx1 != -1 and idx2 != -1 and idx1 < idx2: # Ensure both found and in correct order
        for i in range(idx1 + 1, idx2):
            output_list[i] = fill_value

    # 8. Format the modified list back into a space-separated string for the final output.
    output_str = " ".join(map(str, output_list))

    return output_str
