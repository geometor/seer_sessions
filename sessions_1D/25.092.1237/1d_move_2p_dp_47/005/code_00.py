"""
Treat the input grid as a single, flat list of color values (pixels).
Search the list from left to right to find the starting index (i) of the *first* occurrence of the subsequence [white, white, azure] (represented numerically as [0, 0, 8]). If this marker is not found, return the input list unchanged.
Identify the segment corresponding to the [white, white] part of the found marker. This is the slice input[i : i+2]. Call this the `marker_pair`.
Identify the segment containing all elements *starting from* the azure (8) pixel of the found marker sequence (i.e., from index i+2) to the end of the list. Call this the `trailing_elements`.
Identify the segment containing the initial contiguous block of white (0) pixels at the very beginning of the list. Find the index j of the last pixel in this initial block. If the list does not start with white, this block is empty, and j is effectively -1. Call the segment input[0 : j+1] the `leading_zeros`.
Identify the segment of the list that lies *between* the end of the leading_zeros and the start of the marker_pair. This segment starts at index j+1 and ends just before index i. Call this the `shifting_block` (input[j+1 : i]). Note that this block can be empty if j+1 is equal to i.
Construct the output list by concatenating the identified segments in the following specific order: leading_zeros + marker_pair + shifting_block + trailing_elements.
Return the constructed list as the output.
"""

from typing import List

def find_subsequence_index(sequence: List[int], subsequence: List[int]) -> int:
    """
    Finds the starting index of the first occurrence of a subsequence within a sequence.

    Args:
        sequence: The main list to search within.
        subsequence: The list to search for.

    Returns:
        The starting index of the first occurrence of the subsequence, or -1 if not found.
    """
    for i in range(len(sequence) - len(subsequence) + 1):
        if sequence[i:i + len(subsequence)] == subsequence:
            return i
    return -1 # Not found

def find_last_leading_zero_index(sequence: List[int]) -> int:
    """
    Finds the index of the last leading zero (white pixel, value 0) in a sequence.

    Args:
        sequence: The list to search within.

    Returns:
        The index of the last leading zero, or -1 if the sequence doesn't start with zero.
    """
    last_zero_index = -1
    for i, val in enumerate(sequence):
        if val == 0: # 0 represents white
            last_zero_index = i
        else:
            # Stop as soon as the first non-zero element is encountered
            break 
    return last_zero_index

def transform(input_grid: List[int]) -> List[int]:
    """
    Applies the rearrangement transformation based on the [0, 0, 8] marker.

    Args:
        input_grid: A flat list representing the input grid's pixels.

    Returns:
        A flat list representing the transformed grid's pixels.
    """
    
    # The input is already a flat list, treat it as the sequence
    sequence = input_grid
    
    # Define the marker sequence to search for
    marker = [0, 0, 8] # white, white, azure
    
    # Step 2: Locate the first occurrence of the marker subsequence [0, 0, 8]
    marker_start_index = find_subsequence_index(sequence, marker)
    
    # Handle cases where the marker might not be found
    if marker_start_index == -1:
        # As per the rule, return the original sequence if marker not found
        return sequence 

    # Step 3: Identify the marker_pair segment [0, 0]
    # This is the part of the sequence at marker_start_index and marker_start_index + 1
    marker_pair = sequence[marker_start_index : marker_start_index + 2] 

    # Step 4: Identify the trailing_elements segment (starts from '8' at marker_start_index + 2)
    trailing_elements = sequence[marker_start_index + 2 :]

    # Step 5: Identify the leading_zeros segment
    # Find the index 'j' of the last zero at the very beginning of the sequence
    last_leading_zero_idx = find_last_leading_zero_index(sequence)
    # Extract the leading zeros segment. If last_leading_zero_idx is -1 (no leading zeros), 
    # the slice sequence[0:0] correctly results in an empty list.
    leading_zeros = sequence[0 : last_leading_zero_idx + 1]
    
    # Step 6: Identify the shifting_block segment (between leading zeros and marker)
    # The start index for shifting_block is right after the leading zeros (index j+1)
    shifting_block_start_index = last_leading_zero_idx + 1
    # The end index for shifting_block is right before the marker starts (index i)
    shifting_block_end_index = marker_start_index
    # Extract the shifting block segment. If start >= end, this slice correctly results in an empty list.
    shifting_block = sequence[shifting_block_start_index : shifting_block_end_index]

    # Step 7: Construct the output sequence by concatenating segments in the new order:
    # leading_zeros + marker_pair + shifting_block + trailing_elements
    output_sequence = leading_zeros + marker_pair + shifting_block + trailing_elements
    
    # Step 8: Return the newly constructed sequence
    return output_sequence