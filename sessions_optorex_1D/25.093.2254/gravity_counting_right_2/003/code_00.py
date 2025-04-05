import collections  # Import collections though not strictly needed for this version

"""
Counts the number of non-zero integers in the input sequence (list or array) and generates an output sequence (list) of the same length (12). The output sequence starts with a number of 1s equal to the count of non-zero integers, followed by 0s to fill the remaining positions.
"""

def count_non_zeros(numbers: list[int]) -> int:
    """Counts the number of non-zero elements in a list of integers."""
    count = 0
    for num in numbers:
        if num != 0:
            count += 1
    return count

def transform(input_sequence) -> list[int]:
    """
    Transforms the input sequence according to the described rule.

    Args:
        input_sequence: A list or array containing 12 integers.

    Returns:
        A list containing 12 binary integers (1 or 0).
    """
    # Ensure input is treated as a list if it's an array-like structure
    # (This might be handled by the environment, but being explicit can help)
    input_list = list(input_sequence) 

    # Count the non-zero numbers in the input list
    non_zero_count = count_non_zeros(input_list)

    # Determine the total length (should always be 12 based on examples)
    total_length = len(input_list) # Or simply use 12 if guaranteed

    # Construct the output list
    # Start with 'non_zero_count' number of 1s
    output_sequence = [1] * non_zero_count
    
    # Append the required number of 0s to reach the total length
    output_sequence.extend([0] * (total_length - non_zero_count))

    return output_sequence