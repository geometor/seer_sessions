import numpy as np

"""
Transforms a sequence of digits by performing the following steps:
1. Identify all maximal contiguous subsequences within the input sequence that consist entirely of non-zero digits (1-9). Record the start index, end index, and length for each.
2. Find the subsequence with the maximum length among those identified.
3. If multiple subsequences share the maximum length, select the one that appears earliest in the original sequence (i.e., has the minimum start index).
4. If no non-zero subsequences exist, return the original sequence unchanged.
5. Create a copy of the original sequence.
6. Replace every digit within the selected longest subsequence (from its start index to its end index, inclusive) in the copied sequence with the digit '1'.
7. Return the modified sequence.
"""

def _find_non_zero_subsequences(digits):
    """
    Identifies all maximal contiguous subsequences of non-zero digits.

    Args:
        digits: A list of integers.

    Returns:
        A list of tuples, where each tuple represents a subsequence
        and contains (start_index, end_index, length).
        Returns an empty list if no non-zero subsequences are found or input is empty.
    """
    subsequences = []
    start_index = -1
    n = len(digits)
    if n == 0:
        return [] # Handle empty input

    for i, digit in enumerate(digits):
        # Start of a potential subsequence if digit is non-zero and we are not already in one
        if digit != 0 and start_index == -1:
            start_index = i
        # End of a subsequence if we encounter a zero or reach the end of the list while in a subsequence
        elif (digit == 0 or i == n - 1) and start_index != -1:
            # Determine the correct end index
            end_index = i - 1 if digit == 0 else i
            # Calculate length
            length = end_index - start_index + 1
            # Store the subsequence info
            subsequences.append((start_index, end_index, length))
            # Reset start index to indicate we are no longer in a subsequence
            start_index = -1

    return subsequences

def _find_longest_subsequence(subsequences):
    """
    Finds the longest subsequence from a list of subsequences, breaking ties
    by choosing the one with the earliest start index.

    Args:
        subsequences: A list of tuples (start_index, end_index, length).

    Returns:
        A tuple (start_index, end_index, length) for the longest subsequence,
        or None if the input list is empty.
    """
    if not subsequences:
        return None

    # Initialize with the first subsequence as the longest
    longest_sub = subsequences[0]
    max_len = longest_sub[2] # length is the third element

    # Iterate through the rest of the subsequences
    for sub in subsequences[1:]:
        start, end, length = sub
        # If current subsequence is strictly longer, it becomes the new longest
        if length > max_len:
            max_len = length
            longest_sub = sub
        # If lengths are equal, keep the one with the smaller start index.
        # Since we iterate from left to right, the current `longest_sub`
        # will always have an equal or smaller start index than `sub`
        # if their lengths are equal. So, no explicit update needed for ties.

    return longest_sub


def transform(input_sequence):
    """
    Applies the transformation rule to the input sequence of digits.

    Args:
        input_sequence: A list or numpy array of integers representing the digit sequence.

    Returns:
        A list of integers representing the transformed sequence.
    """
    # Ensure input is a standard list for consistent handling and modification
    if isinstance(input_sequence, np.ndarray):
        input_list = input_sequence.tolist()
    else:
        # Assume it's already list-like, ensure it's a mutable list
        input_list = list(input_sequence)

    # 1. Create a working copy of the input sequence.
    output_sequence = list(input_list)

    # 2. Identify all maximal contiguous non-zero subsequences.
    subsequences = _find_non_zero_subsequences(input_list)

    # 3. If no non-zero subsequences found, return the original (copied) sequence.
    if not subsequences:
        return output_sequence

    # 4. Find the longest subsequence (handles tie-breaking by start index).
    longest_sub = _find_longest_subsequence(subsequences)

    # 5. If a longest subsequence was found (should always be true if subsequences is not empty)
    if longest_sub:
        # Unpack the start and end indices from the result
        start_index, end_index, _ = longest_sub
        
        # 6. Iterate through the indices of the selected subsequence in the output copy.
        for i in range(start_index, end_index + 1):
            # Set the value at each index to 1.
            output_sequence[i] = 1

    # 7. Return the modified sequence.
    return output_sequence