import collections
import math # Although not used in the final code, common math/science libs are available
import numpy as np # Import numpy as the error suggests array-like input

"""
Transforms an input sequence of digits by:
1. Parsing the input into a list of integers. The input is often a space-separated string.
2. Identifying the most frequent non-zero digit in the list. (Assumes a unique most frequent non-zero digit).
3. Finding the longest consecutive run (sequence) of this most frequent digit. (Assumes a unique longest run for that digit).
4. Replacing the digits within this specific longest run with the digit 1 in a copy of the list.
5. All other digits (including zeros and digits not part of the target run) remain unchanged. Zeros act as separators and are never modified.
If no non-zero digits exist, or the input is empty/invalid, the original sequence (or an empty list) is returned.
"""

def _parse_input(input_data):
    """
    Parses various input formats (string, list, tuple, iterable) into a list of integers.
    Handles potential errors during conversion. Returns empty list for invalid/unparseable input.
    """
    if isinstance(input_data, str):
        # Handle space-separated string input
        try:
            # Filter out empty strings that might result from multiple spaces
            parts = [p for p in input_data.split() if p]
            return [int(x) for x in parts]
        except ValueError:
            # Handle case where split results in non-integer strings
            return []
    elif isinstance(input_data, (list, tuple)):
        # Handle list or tuple input
        try:
            return [int(x) for x in input_data]
        except (ValueError, TypeError):
             # Handle case where list contains non-numeric types
             return []
    elif hasattr(input_data, '__iter__'): # More general check for iterables like numpy arrays
        # Handle numpy arrays or other iterables
        try:
             # Attempt conversion, handle potential non-numeric elements
             return [int(x) for x in input_data]
        except (ValueError, TypeError):
             return []
    else:
        # Input is not in a recognizable format
        return []


def _find_most_frequent_non_zero(numbers):
    """
    Finds the most frequent non-zero digit in a list of numbers.
    Assumes no ties for the most frequent digit based on problem constraints.

    Args:
        numbers: A list of integers.

    Returns:
        The most frequent non-zero integer, or None if no non-zero digits exist.
    """
    # Filter out zeros to focus on relevant digits
    non_zeros = [n for n in numbers if n != 0]

    # Handle case where the list contains only zeros or is empty after filtering
    if not non_zeros:
        return None

    # Count frequencies of the non-zero numbers
    counts = collections.Counter(non_zeros)

    # Find the digit (key) with the maximum frequency (value)
    # The problem statement implies uniqueness, so simple max is sufficient.
    # max(counts, key=counts.get) returns the key with the highest value
    most_frequent_digit = max(counts, key=counts.get) # Use counts.get as the key function

    return most_frequent_digit

def _find_longest_run(numbers, target_digit):
    """
    Finds the start index, end index (inclusive), and length of the longest
    consecutive run of target_digit in the numbers list.
    Assumes a unique longest run if multiple runs exist, based on problem constraints.

    Args:
        numbers: A list of integers.
        target_digit: The integer value whose longest run is sought.

    Returns:
        A tuple (start_index, end_index, length). Returns (-1, -1, 0) if
        the target_digit is not found or has no runs.
    """
    longest_run_start = -1
    longest_run_end = -1
    max_length = 0

    current_run_start = -1
    current_length = 0

    # Iterate through the list with index
    for i, num in enumerate(numbers):
        if num == target_digit:
            # If this is the start of a new run of the target digit
            if current_length == 0:
                current_run_start = i
            # Increment the length of the current run
            current_length += 1
        else:
            # If a run of the target digit just ended (or we are not in a run)
            if current_length > 0:
                # Check if the run that just ended is longer than the max found so far
                if current_length > max_length:
                    max_length = current_length
                    longest_run_start = current_run_start
                    longest_run_end = i - 1 # The run ended at the previous index
            # Reset the current run tracking since the sequence broke
            current_run_start = -1 # Redundant, but clear
            current_length = 0

    # After the loop, check if the longest run was at the very end of the list
    # This handles cases where the list ends with the longest run
    if current_length > 0:
        if current_length > max_length:
            max_length = current_length
            longest_run_start = current_run_start
            # The run extends to the last index of the list
            longest_run_end = len(numbers) - 1

    # Return the details of the longest run found
    if max_length > 0:
        return longest_run_start, longest_run_end, max_length
    else:
        # Target digit not found, or it never appeared consecutively
        return -1, -1, 0

def transform(input_data):
    # 1. Parse the input data (e.g., string) into a list of integers.
    input_list = _parse_input(input_data)

    # Handle cases where parsing failed or resulted in an empty list.
    if not input_list:
        return [] # Return empty list as per convention for invalid/empty input.

    # 2. Create a mutable copy of the input list to modify.
    output_list = list(input_list)

    # 3. Identify the most frequent non-zero digit.
    target_digit = _find_most_frequent_non_zero(input_list)

    # 4. If no non-zero digits exist (target_digit is None), return the unmodified copy.
    if target_digit is None:
        return output_list

    # 5. Find the longest consecutive run of the target digit.
    # Get the start index, end index (inclusive), and length of this run.
    start_index, end_index, length = _find_longest_run(input_list, target_digit)

    # 6. If a run was found (length > 0), modify the output list.
    if length > 0:
        # Iterate through the indices belonging to the longest run.
        for i in range(start_index, end_index + 1):
            # Replace the digit at the current index with 1.
            # Bounds are guaranteed by the logic in _find_longest_run.
            output_list[i] = 1

    # 7. Return the potentially modified list.
    return output_list