import numpy as np

"""
Transforms a sequence of digits by finding the longest contiguous subsequence
of non-zero digits and replacing all digits within that subsequence with 1.
If multiple subsequences share the maximum length, the one appearing earliest
(smallest start index) in the sequence is chosen.
"""

def _find_non_zero_subsequences(digits):
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
    Finds the longest subsequence from a list of subsequences.

    Args:
        subsequences: A list of tuples (start_index, end_index, length).

    Returns:
        A tuple (start_index, end_index, length) for the longest subsequence,
        or None if the input list is empty. If multiple subsequences
        share the maximum length, the one with the smallest start_index is returned.
    """
    if not subsequences:
        return None

    # Initialize with the first subsequence as the longest
    longest_sub = subsequences[0]
    max_len = longest_sub[2] # length is the third element

    # Iterate through the rest of the subsequences
    for sub in subsequences[1:]:
        start, end, length = sub
        # If current subsequence is longer, it becomes the new longest
        if length > max_len:
            max_len = length
            longest_sub = sub
        # If lengths are equal, keep the one with the smaller start index (already handled by iteration order)
        # No need for specific tie-breaking logic here if we just update when strictly greater.

    return longest_sub


def transform(input_sequence):
    """
    Applies the transformation rule to the input sequence of digits.
    Identifies the longest contiguous subsequence of non-zero digits
    and replaces its elements with '1'.

    Args:
        input_sequence: A list or numpy array of integers.

    Returns:
        A list of integers representing the transformed sequence.
    """
    # Ensure input is a standard list for consistent handling
    if isinstance(input_sequence, np.ndarray):
        input_list = input_sequence.tolist()
    else:
        # Assume it's already list-like or convert just in case
        input_list = list(input_sequence)

    # Initialize output_sequence as a copy of the input list
    output_sequence = list(input_list)

    # Step 1: Identify all maximal contiguous non-zero subsequences
    subsequences = _find_non_zero_subsequences(input_list)

    # Step 2: Find the longest subsequence (returns None if no subsequences found)
    longest_sub = _find_longest_subsequence(subsequences)

    # Step 3: If a longest subsequence was found, modify the output sequence
    if longest_sub:
        # Unpack the start and end indices from the result
        start_index, end_index, _ = longest_sub
        # Iterate through the indices of the longest subsequence
        for i in range(start_index, end_index + 1):
            # Change the digit at the current index to 1 in the output sequence
            output_sequence[i] = 1

    # Step 4: Return the modified sequence
    # Assuming the test environment expects a list or handles conversion
    return output_sequence