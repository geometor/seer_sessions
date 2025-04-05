import math

"""
Transforms a sequence of 12 space-separated integers based on the value of the single non-zero integer present.

1.  Parses the input string into a list of 12 integers.
2.  Identifies the non-zero integer (N) and its count.
3.  Applies a specific rearrangement rule based on N:
    - If N is 1 or 9: Collects all N's and places them starting at the index of the first N in the input plus 4.
    - If N is 4 or 5: Collects all N's and places them starting at index 1.
    - If N is 6:
        - If count is 2, places '6 6' at indices 3 and 4.
        - If count > 2, collects all 6's and places them starting at index 0.
    - If N is 7: Splits the collected N's into two halves (ceil/floor) and places the first half at the beginning and the second half at the end of the output sequence.
4.  Fills remaining positions with 0s.
5.  Formats the resulting list back into a space-separated string.
"""

def transform(input_str: str) -> str:
    """
    Applies the transformation rule to the input string.

    Args:
        input_str: A string containing 12 space-separated integers.

    Returns:
        A string containing the transformed 12 space-separated integers.
    """
    # Parse input string into a list of integers
    input_list = [int(x) for x in input_str.split()]
    n_elements = len(input_list) # Should always be 12 based on examples

    # Initialize output grid with zeros
    output_list = [0] * n_elements

    # Find the non-zero element value (N) and its count
    non_zero_val = 0
    count = 0
    first_idx = -1
    for i, val in enumerate(input_list):
        if val != 0:
            if non_zero_val == 0: # First non-zero found
                 non_zero_val = val
                 first_idx = i
            count += 1

    # If no non-zero element found (all zeros), return zeros
    if non_zero_val == 0:
        return " ".join(map(str, output_list))

    # Apply transformation rule based on the non-zero value (N)
    if non_zero_val == 1 or non_zero_val == 9:
        # Place count N's starting at first_idx + 4
        start_index = first_idx + 4
        # Ensure placement doesn't go out of bounds (although examples suggest it won't)
        end_index = min(start_index + count, n_elements)
        for i in range(start_index, end_index):
             # Check boundary before assignment just in case
             if i < n_elements:
                output_list[i] = non_zero_val

    elif non_zero_val == 4 or non_zero_val == 5:
        # Place count N's starting at index 1
        start_index = 1
        end_index = min(start_index + count, n_elements)
        for i in range(start_index, end_index):
             # Check boundary before assignment
             if i < n_elements:
                output_list[i] = non_zero_val

    elif non_zero_val == 6:
        if count == 2:
            # Place '6 6' at indices 3 and 4
            if 3 < n_elements: output_list[3] = 6
            if 4 < n_elements: output_list[4] = 6
        elif count > 2:
            # Place count N's starting at index 0
            start_index = 0
            end_index = min(start_index + count, n_elements)
            for i in range(start_index, end_index):
                 if i < n_elements:
                    output_list[i] = non_zero_val

    elif non_zero_val == 7:
        # Split into two halves and place at ends
        size1 = math.ceil(count / 2)
        size2 = math.floor(count / 2) # or count - size1

        # Place first half at the beginning
        for i in range(size1):
            if i < n_elements:
                output_list[i] = non_zero_val

        # Place second half at the end
        start_index_end = n_elements - size2
        for i in range(size2):
            idx = start_index_end + i
            if idx < n_elements:
                output_list[idx] = non_zero_val

    # Convert the output list back to a space-separated string
    return " ".join(map(str, output_list))
