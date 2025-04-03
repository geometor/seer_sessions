import math

def _find_first_last_nonzero(sequence):
    """Finds the index of the first and last non-zero element in a sequence."""
    first_nonzero_index = None
    last_nonzero_index = None
    for i, val in enumerate(sequence):
        if val != 0:
            if first_nonzero_index is None:
                first_nonzero_index = i
            last_nonzero_index = i
    return first_nonzero_index, last_nonzero_index

def transform(input_str: str) -> str:
    """
    Transforms a sequence of digits represented as a space-separated string.
    It identifies the contiguous subsequence starting with the first non-zero
    digit and ending with the last non-zero digit. This subsequence is then
    shifted left by two positions (or fewer if it would shift past the beginning),
    and the sequence is padded with zeros to maintain the original length.
    If the input contains only zeros, it is returned unchanged.
    """
    # 1. Receive the input sequence of digits.
    # Convert string input to list of integers
    input_sequence = [int(x) for x in input_str.split()]
    original_length = len(input_sequence)

    # 2. Find the index of the first non-zero digit and last non-zero digit.
    first_nonzero_index, last_nonzero_index = _find_first_last_nonzero(input_sequence)

    # If no non-zero digit exists, return the original input sequence.
    if first_nonzero_index is None:
        return input_str # Return original string format

    # 4. Extract the 'core sequence'.
    core_sequence = input_sequence[first_nonzero_index : last_nonzero_index + 1]

    # 5. Calculate the starting index for the core sequence in the output.
    # Take the index of the first non-zero digit and subtract 2.
    # If the result is negative, use 0 instead.
    output_start_index = max(0, first_nonzero_index - 2)

    # 6. Construct the output sequence.
    # a. Start with leading zeros.
    leading_zeros = [0] * output_start_index

    # b. Append the core sequence.
    output_sequence_parts = leading_zeros + core_sequence

    # c. Append trailing zeros until the total length matches the original.
    num_trailing_zeros = original_length - len(output_sequence_parts)
    trailing_zeros = [0] * num_trailing_zeros
    output_sequence = output_sequence_parts + trailing_zeros

    # 7. Return the constructed output sequence.
    # Convert list of integers back to space-separated string
    output_str = " ".join(map(str, output_sequence))
    return output_str
