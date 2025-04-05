"""
Identifies the initial contiguous segment of non-zero numbers (non_zero_prefix) in the input list. 
Checks if the length of this prefix (P) is positive and even. 
If valid, determines the repeating base_pattern by taking the first P/2 elements of the prefix. 
Constructs the output list by starting with the non_zero_prefix and repeatedly 
appending elements from the base_pattern (cycling through the pattern) until the 
output list's length matches the original input list's length (L).
If the prefix length P is 0 or odd, returns a list of L zeros.
"""

from typing import List

# Helper function to find the end of the initial non-zero segment
def _find_non_zero_segment_end(sequence: List[int]) -> int:
    """Finds the index of the first zero element, or returns the sequence length if no zero is found."""
    for i, num in enumerate(sequence):
        if num == 0:
            return i
    return len(sequence)

# Helper function to extract the base pattern if the prefix is valid
def _extract_base_pattern(non_zero_segment: List[int]) -> List[int]:
    """
    Extracts the base pattern from the non-zero segment if its length P is positive and even.
    Assumes the segment represents two repetitions of the pattern in valid cases.
    Returns an empty list if the segment is empty or has odd length.
    """
    segment_length = len(non_zero_segment)
    # Check for validity: positive and even length
    if segment_length > 0 and segment_length % 2 == 0:
        pattern_length = segment_length // 2
        # Optional verification (consistent with observations):
        # if non_zero_segment[:pattern_length] == non_zero_segment[pattern_length:]:
        #     return non_zero_segment[:pattern_length]
        # else: # Prefix doesn't consist of two identical halves
        #     return [] 
        # Strict interpretation based only on length check:
        return non_zero_segment[:pattern_length]
    else:
        # Invalid segment (empty or odd length)
        return []

def transform(input_sequence: List[int]) -> List[int]:
    """
    Transforms the input sequence based on the identified repeating pattern.

    Args:
        input_sequence: A list of integers, potentially with trailing zeros.

    Returns:
        A list of integers where trailing zeros are replaced by repeating the base pattern,
        or a list of zeros if the pattern is invalid.
    """
    # 1. Get the total length of the input list.
    total_length = len(input_sequence)
    if total_length == 0:
        return [] # Handle empty input

    # 2. Find the end index of the initial non-zero prefix.
    non_zero_end_index = _find_non_zero_segment_end(input_sequence)
    
    # 3. Extract the non_zero_prefix.
    non_zero_prefix = input_sequence[:non_zero_end_index]
    
    # 4. Attempt to derive the base_pattern from the prefix.
    #    _extract_base_pattern handles checks for positive and even length.
    base_pattern = _extract_base_pattern(non_zero_prefix)
    
    # 5. Check if a valid base_pattern was found (i.e., prefix length > 0 and even).
    #    Use explicit length check for robustness against potential type issues (e.g., numpy arrays).
    if len(base_pattern) == 0:
        # If pattern is invalid (prefix was empty or odd length), return L zeros.
        output_sequence = [0] * total_length
    else:
        # 6. If pattern is valid, initialize the output with the non_zero_prefix.
        output_sequence = list(non_zero_prefix) # Create a copy
        pattern_length = len(base_pattern)
        pattern_index = 0

        # 7. Fill the remainder of the output list by cycling through the base_pattern.
        while len(output_sequence) < total_length:
            output_sequence.append(base_pattern[pattern_index])
            pattern_index = (pattern_index + 1) % pattern_length # Cycle index

    # 8. Return the final constructed output list.
    return output_sequence