import collections
import math  # Although not used in the final code, common math/science libs are available

def _find_most_frequent_non_zero(numbers):
    """
    Finds the most frequent non-zero digit in a list of numbers.
    Assumes no ties for the most frequent digit based on problem constraints.

    Args:
        numbers: A list of integers.

    Returns:
        The most frequent non-zero integer, or None if no non-zero digits exist.
    """
    # Filter out zeros
    non_zeros = [n for n in numbers if n != 0]
    
    # Handle case where there are no non-zero numbers
    if not non_zeros:
        return None

    # Count frequencies of non-zero numbers
    counts = collections.Counter(non_zeros)
    
    # Find the digit with the maximum frequency
    # max(counts, key=counts.get) returns the key (digit) with the highest value (count)
    most_frequent_digit = max(counts, key=counts.get)
    
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

    for i, num in enumerate(numbers):
        if num == target_digit:
            # If this is the start of a new run
            if current_length == 0:
                current_run_start = i
            # Increment current run length
            current_length += 1
        else:
            # If a run just ended
            if current_length > 0:
                # Check if this just-ended run is the new longest
                if current_length > max_length:
                    max_length = current_length
                    longest_run_start = current_run_start
                    longest_run_end = i - 1 # End index is the previous element
            # Reset current run tracking
            current_run_start = -1
            current_length = 0

    # Special check: Handle case where the longest run is at the very end of the list
    if current_length > 0:
        if current_length > max_length:
            max_length = current_length
            longest_run_start = current_run_start
            longest_run_end = len(numbers) - 1 # End index is the last element

    # Return the findings
    if max_length > 0:
        return longest_run_start, longest_run_end, max_length
    else:
        # Target digit not found or no runs
        return -1, -1, 0

def transform(input_list):
    """
    Transforms the input list by finding the longest consecutive run of the
    most frequent non-zero digit and replacing the digits in that specific run
    with the digit 1. All other digits remain unchanged.

    Args:
        input_list: A list of single-digit integers.

    Returns:
        A new list of integers representing the transformed input.
    """
    # Handle empty input list case
    if not input_list:
        return []

    # Initialize output_list as a copy of the input to avoid modifying the original
    output_list = list(input_list)

    # Step 1: Find the most frequent non-zero digit.
    target_digit = _find_most_frequent_non_zero(input_list)

    # If no non-zero digits were found (target_digit is None), no transformation needed.
    if target_digit is None:
        return output_list

    # Step 2 & 3: Find the longest consecutive run of the target digit.
    # This returns the start index, end index (inclusive), and length of that run.
    start_index, end_index, length = _find_longest_run(input_list, target_digit)

    # Step 4: If a longest run was found (length > 0), replace its digits with 1.
    if length > 0:
        # Iterate through the indices of the longest run
        for i in range(start_index, end_index + 1):
            # Make sure the index is valid (should always be true based on find_longest_run logic)
             if 0 <= i < len(output_list):
                 # Replace the digit at this position with 1 in the output list
                 output_list[i] = 1

    # Step 5: Return the modified list.
    return output_list