"""
The transformation rule operates on a sequence of single-digit integers.
It identifies the first occurrence of the digit '2'. If found, it then searches
for the first non-zero digit ('X') that appears *after* this '2'.
If the sequence of digits strictly between the first '2' and the first 'X'
consists entirely of one or more zeros, then all these zeros are replaced
by the digit 'X'. Otherwise, the sequence remains unchanged. If '2' is not
found, or if no non-zero digit 'X' is found after the first '2', the sequence
also remains unchanged.
"""

import math  # math is generally useful, though not strictly needed here

def transform(input_sequence):
    """
    Applies the transformation rule to the input sequence.

    Args:
        input_sequence: A list of single-digit integers.

    Returns:
        A new list of integers representing the transformed sequence.
    """
    output_sequence = list(input_sequence) # Create a copy to modify

    # 1. Find the index of the first occurrence of the digit 2.
    try:
        first_2_index = output_sequence.index(2)
    except ValueError:
        # If 2 is not present, return the original sequence unchanged.
        return output_sequence

    # 2. Initialize search starting from the index immediately following the first 2.
    start_scan_index = first_2_index + 1
    first_x_index = -1
    first_x_value = -1

    # 3. Scan the sequence to the right to find the first non-zero digit X.
    for i in range(start_scan_index, len(output_sequence)):
        if output_sequence[i] != 0:
            first_x_index = i
            first_x_value = output_sequence[i]
            break # Stop at the first non-zero digit

    # 4. Check if a non-zero digit X was found.
    if first_x_index == -1:
        # No non-zero digit found after the first 2. Return unchanged.
        return output_sequence

    # 5. Examine the subsequence between the first 2 (exclusive) and X (exclusive).
    #    Check if it consists entirely of one or more zeros.
    subsequence_start = first_2_index + 1
    subsequence_end = first_x_index # Exclusive end index

    # Check if the subsequence is non-empty
    if subsequence_start < subsequence_end:
        all_zeros = True
        for i in range(subsequence_start, subsequence_end):
            if output_sequence[i] != 0:
                all_zeros = False
                break

        # 6. If the subsequence consists of one or more zeros, replace them.
        if all_zeros:
            for i in range(subsequence_start, subsequence_end):
                output_sequence[i] = first_x_value
            # Return the modified sequence
            return output_sequence
        else:
            # Subsequence contains non-zeros. Return unchanged.
            return list(input_sequence) # Return original state
    else:
        # Subsequence is empty (X immediately follows 2). Return unchanged.
         return list(input_sequence) # Return original state
