import math
import collections

"""
Transforms a sequence of digits by finding the longest contiguous subsequence of identical non-zero digits. 
If multiple such subsequences share the maximum length, the leftmost one is chosen. 
The digits within the chosen subsequence are then replaced with the digit 1. 
If no non-zero homogeneous subsequence is found, the original sequence is returned unchanged.
"""

def _find_homogeneous_nonzero_subsequences(int_list):
    """
    Identifies all contiguous subsequences of identical non-zero digits.

    Args:
        int_list: A list of integers representing the input sequence.

    Returns:
        A list of tuples, where each tuple represents a subsequence
        and contains (start_index, length, value). Returns an empty
        list if no such subsequences are found.
    """
    subsequences = []
    if not int_list:
        return subsequences

    i = 0
    n = len(int_list)
    while i < n:
        current_digit = int_list[i]
        # Start searching only if the current digit is non-zero
        if current_digit != 0:
            start_index = i
            j = i + 1
            # Extend the subsequence as long as the digit matches and we are within bounds
            while j < n and int_list[j] == current_digit:
                j += 1
            # Calculate the length of the found subsequence
            length = j - i
            # Record the subsequence details
            subsequences.append((start_index, length, current_digit))
            # Advance the main loop index past the found subsequence
            i = j
        else:
            # If the digit is zero, just move to the next position
            i += 1
            
    return subsequences

def transform(input_str: str) -> str:
    """
    Applies the transformation rule to the input string sequence.

    Args:
        input_str: A string of space-separated integers.

    Returns:
        A string of space-separated integers representing the transformed sequence.
    """
    # 1. Parse the input string into a list of integers.
    try:
        input_list = [int(x) for x in input_str.split()]
    except ValueError:
        # Handle potential errors if input is not numbers
        print(f"Error: Input string '{input_str}' contains non-integer values.")
        return input_str # Or raise an error, depending on desired behavior

    # Initialize the output list as a copy of the input
    output_list = list(input_list)

    # 2. Find all contiguous homogeneous non-zero subsequences.
    subsequences = _find_homogeneous_nonzero_subsequences(input_list)

    # 3. If no such subsequences are found, return the original sequence string.
    if not subsequences:
        return input_str

    # 4. Determine the maximum length among the found subsequences.
    max_len = 0
    for _, length, _ in subsequences:
        if length > max_len:
            max_len = length

    # 5. Identify all subsequences that have this maximum length.
    longest_subs = []
    for sub in subsequences:
        if sub[1] == max_len:
            longest_subs.append(sub)

    # 6. Select the leftmost subsequence among those with the maximum length.
    # Since subsequences are found left-to-right, the first one in longest_subs
    # matching max_len will be the leftmost. We can sort by start_index for robustness.
    longest_subs.sort(key=lambda x: x[0]) 
    target_sub = longest_subs[0]
    start_index = target_sub[0]
    length = target_sub[1]

    # 7. Modify the output list: change digits in the selected subsequence to 1.
    for i in range(start_index, start_index + length):
        # Ensure index is within bounds (should be, but good practice)
        if 0 <= i < len(output_list):
            output_list[i] = 1

    # 8. Convert the modified list back into a space-separated string.
    output_str = " ".join(map(str, output_list))

    return output_str
