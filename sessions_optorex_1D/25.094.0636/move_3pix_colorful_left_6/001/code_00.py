import math
import re # Using re for potentially simpler parsing if needed, though split() is likely sufficient

"""
Transforms a sequence of 12 digits based on the following rule:
1. Identify the subsequence (segment) starting from the first non-zero digit and ending at the last non-zero digit in the input sequence. This segment includes any zeros within it.
2. If no non-zero digits are found, the output is a sequence of 12 zeros.
3. Calculate the target starting index for this segment in the output sequence by subtracting 3 from the original starting index. Ensure the target index is not less than 0 (i.e., use max(0, original_start_index - 3)).
4. Construct the output sequence of length 12, initially filled with zeros.
5. Place the extracted segment into the output sequence starting at the calculated target index.
6. Return the resulting sequence.
"""

def transform(input_str: str) -> str:
    """
    Applies the described segment shifting transformation to the input string.

    Args:
        input_str: A string containing 12 space-separated digits.

    Returns:
        A string containing 12 space-separated digits representing the transformed sequence.
    """

    # Parse the input string into a list of integers
    input_digits = [int(d) for d in input_str.split()]
    n = len(input_digits) # should be 12 based on examples

    # 1. Find the index of the first non-zero digit (start_index)
    start_index = -1
    for i, digit in enumerate(input_digits):
        if digit != 0:
            start_index = i
            break

    # 2. Handle the case where all digits are zero
    if start_index == -1:
        # If no non-zero digits, return a string of 12 zeros
        return " ".join(['0'] * n)

    # 3. Find the index of the last non-zero digit (end_index)
    end_index = -1
    for i in range(n - 1, -1, -1): # Iterate backwards
        if input_digits[i] != 0:
            end_index = i
            break
    
    # This check should technically not be needed if start_index != -1, 
    # but added for robustness, though end_index will always be >= start_index here.
    # if end_index == -1: end_index = start_index 

    # 4. Extract the segment
    # Slicing goes up to, but does not include, the end value, so add 1 to end_index
    segment = input_digits[start_index : end_index + 1]

    # 5. Calculate the new starting position for the segment
    shift_amount = 3
    new_start_index = max(0, start_index - shift_amount)

    # 6. Construct the output sequence
    # Initialize output with zeros
    output_digits = [0] * n

    # Calculate where the segment ends in the output grid
    # Ensure the segment doesn't exceed the bounds of the output grid
    segment_len = len(segment)
    place_end_index = new_start_index + segment_len

    # Place the segment into the output list
    # The slicing handles the length automatically
    output_digits[new_start_index:place_end_index] = segment

    # 7. Format the output list back into a space-separated string
    output_str = " ".join(map(str, output_digits))

    return output_str
