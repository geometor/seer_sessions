import math
import collections

"""
Identifies the first occurrence of a non-zero number followed immediately by a zero in the input sequence.
Let the index of this zero be 'm'.
Identifies the contiguous block of non-zero numbers ending at index 'm-1'. Let the start index of this block be 'k'.
If the block starts at the beginning of the sequence (k=0), swap the last element of the block (at m-1) with the zero (at m).
If the block does not start at the beginning (k>0), the transformation effectively shifts the block one position to the left and moves the zero that preceded the block (at index k-1) to the position immediately after the shifted block (which corresponds to the original index m-1).
If no non-zero number followed by a zero is found, the input sequence is returned unchanged.
"""

def _find_trigger_index(sequence):
    """
    Find the index 'm' of the first zero that is immediately preceded by a non-zero number.
    Returns -1 if no such index is found.
    """
    for m in range(1, len(sequence)):
        if sequence[m] == 0 and sequence[m-1] != 0:
            return m
    return -1 # Indicate that the pattern was not found

def _find_block_start(sequence, block_end_index):
    """
    Find the starting index 'k' of a contiguous block of non-zero numbers
    that ends at the given block_end_index.
    """
    k = block_end_index
    # Move backwards from the end of the block as long as we are within bounds
    # and the element is non-zero.
    while k >= 0 and sequence[k] != 0:
        k -= 1
    # The block starts at the index immediately after the last zero encountered
    # (or at index 0 if no preceding zero was found).
    return k + 1

def transform(input_sequence):
    """
    Applies the transformation rule to the input sequence.

    Args:
        input_sequence: A list of integers.

    Returns:
        A new list of integers representing the transformed sequence.
    """
    n = len(input_sequence)
    # Work on a copy to avoid modifying the original input list
    output_sequence = list(input_sequence)

    # 1. Find the index 'm' of the first zero preceded by a non-zero number.
    m = _find_trigger_index(output_sequence)

    # 2. If the trigger pattern (non-zero followed by zero) is not found,
    #    return the original sequence copy.
    if m == -1:
        return output_sequence

    # 3. Determine the start index 'k' of the non-zero block ending just before 'm'.
    #    The block ends at index m-1.
    k = _find_block_start(output_sequence, m - 1)

    # 4. Apply the transformation based on whether the block starts at the beginning (k=0).
    if k == 0:
        # Case: The non-zero block starts at the very beginning of the sequence.
        # Swap the last element of the block (at index m-1) with the triggering zero (at index m).
        output_sequence[m-1], output_sequence[m] = output_sequence[m], output_sequence[m-1]
    else:
        # Case: The non-zero block starts after index 0 (i.e., k > 0).
        # This means there is a zero at index k-1.
        # The transformation involves rearranging the parts:
        # - The part of the sequence before the zero at k-1.
        # - The non-zero block itself (from k to m-1).
        # - The zero that was originally at k-1.
        # - The part of the sequence starting from index m+1 (after the triggering zero).

        # Extract the relevant components:
        prefix = output_sequence[0 : k-1]          # Elements before the zero at k-1
        block = output_sequence[k : m]             # The contiguous non-zero block
        zero_before_block = [output_sequence[k-1]] # The zero element originally at k-1
        suffix = output_sequence[m+1 : ]           # Elements after the triggering zero at m

        # Reconstruct the sequence with the block shifted left and the preceding zero moved after it.
        # The resulting sequence effectively has the block starting at k-1,
        # followed by the zero from k-1, followed by the original suffix.
        output_sequence = prefix + block + zero_before_block + suffix

    # Return the transformed sequence
    return output_sequence