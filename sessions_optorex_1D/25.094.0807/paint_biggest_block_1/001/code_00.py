import re

"""
Transforms a sequence of digits based on the following rule:
1. Parse the input string into a list of digits.
2. Identify all maximal contiguous subsequences within the list that consist entirely of non-zero digits.
3. Find the subsequence with the maximum length among these. If there are ties, the specific choice among the longest ones doesn't matter based on the examples, but we'll consistently choose the first one encountered.
4. Replace every digit within the selected longest non-zero subsequence with the digit '1'.
5. Return the modified sequence as a space-separated string.
"""

def find_non_zero_subsequences(digits):
    """
    Identifies all maximal contiguous subsequences of non-zero digits.

    Args:
        digits: A list of integers.

    Returns:
        A list of tuples, where each tuple represents a subsequence
        and contains (start_index, end_index, length).
        Returns an empty list if no non-zero subsequences are found.
    """
    subsequences = []
    start_index = -1
    n = len(digits)

    for i, digit in enumerate(digits):
        # Start of a potential subsequence
        if digit != 0 and start_index == -1:
            start_index = i
        # End of a subsequence (encountering 0 or end of list)
        elif (digit == 0 or i == n - 1) and start_index != -1:
            # Determine the end index
            end_index = i - 1 if digit == 0 else i
            length = end_index - start_index + 1
            subsequences.append((start_index, end_index, length))
            start_index = -1 # Reset for the next potential subsequence

    return subsequences

def find_longest_subsequence(subsequences):
    """
    Finds the longest subsequence from a list of subsequences.

    Args:
        subsequences: A list of tuples (start_index, end_index, length).

    Returns:
        A tuple (start_index, end_index) for the longest subsequence,
        or None if the input list is empty. If multiple subsequences
        share the maximum length, the first one encountered is returned.
    """
    if not subsequences:
        return None

    max_len = -1
    longest_sub_indices = None

    for start, end, length in subsequences:
        if length > max_len:
            max_len = length
            longest_sub_indices = (start, end)

    return longest_sub_indices


def transform(input_string):
    """
    Applies the transformation rule to the input string of digits.
    Identifies the longest contiguous subsequence of non-zero digits
    and replaces its elements with '1'.

    Args:
        input_string: A space-separated string of digits.

    Returns:
        A space-separated string of digits representing the transformed sequence.
    """
    # 1. Parse the input string into a list of digits.
    if not input_string.strip():
        return ""
    input_digits = [int(d) for d in input_string.split()]
    output_digits = list(input_digits) # Create a copy to modify

    # 2. Identify all maximal contiguous non-zero subsequences.
    subsequences = find_non_zero_subsequences(input_digits)

    # 3. Find the longest subsequence.
    longest_sub = find_longest_subsequence(subsequences)

    # 4. Replace digits in the longest subsequence with '1'.
    if longest_sub:
        start, end = longest_sub
        for i in range(start, end + 1):
            output_digits[i] = 1

    # 5. Convert the modified list back to a space-separated string.
    return " ".join(map(str, output_digits))
