import numpy as np
from typing import List

"""
Transformation Rule:
Treat the input grid as a single, flat list of color values (pixels).
Search the list from left to right to find the starting position (index `i`) of the first occurrence of the subsequence [white, white, azure] (represented numerically as [0, 0, 8]).
Identify the segment corresponding to the [white, white] part of the found subsequence. Call this the `marker_pair`.
Identify the segment containing all elements *from* the azure (8) pixel of the found subsequence to the end of the list. Call this the `trailing_elements`.
Identify the segment containing the initial contiguous block of white (0) pixels at the very start of the list. Find the index `j` of the last pixel in this initial block. If the list does not start with white, this block is empty, and `j` is effectively -1. Call the segment the `leading_zeros`.
Identify the segment of the list that lies *between* the `leading_zeros` and the `marker_pair`. This segment starts at index `j+1` and ends at index `i-1`. Call this the `shifting_block`.
Construct the output list by concatenating the identified segments in the following specific order: `leading_zeros` + `marker_pair` + `shifting_block` + `trailing_elements`.
Return the constructed list as the output.
"""


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
    Finds the index of the last leading zero (white pixel) in a sequence.

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
    
    # 1. Locate the first occurrence of the marker subsequence [0, 0, 8]
    marker_start_index = find_subsequence_index(sequence, marker)
    
    # Handle cases where the marker might not be found (though examples suggest it's always present)
    if marker_start_index == -1:
        print("Warning: Marker sequence [0, 0, 8] not found. Returning original sequence.")
        return sequence 

    # 2. Identify the marker_pair segment [0, 0]
    # This is the part of the sequence at marker_start_index and marker_start_index + 1
    marker_pair = sequence[marker_start_index : marker_start_index + 2] 

    # 3. Identify the trailing_elements segment (starts from '8' at marker_start_index + 2)
    trailing_elements = sequence[marker_start_index + 2 :]

    # 4. Identify the leading_zeros segment
    # Find the index of the last zero at the very beginning of the sequence
    last_leading_zero_idx = find_last_leading_zero_index(sequence)
    
    # Extract the leading zeros segment. If last_leading_zero_idx is -1, this slice is empty.
    leading_zeros = sequence[0 : last_leading_zero_idx + 1]
    
    # 5. Identify the shifting_block segment (between leading zeros and marker)
    # The start index for shifting_block is right after the leading zeros (or index 0 if no leading zeros)
    shifting_block_start_index = last_leading_zero_idx + 1
    # The end index for shifting_block is right before the marker starts
    shifting_block_end_index = marker_start_index
    # Extract the shifting block segment. If start >= end, this slice is empty.
    shifting_block = sequence[shifting_block_start_index : shifting_block_end_index]

    # 6. Construct the output sequence by concatenating segments in the new order:
    # leading_zeros + marker_pair + shifting_block + trailing_elements
    output_sequence = leading_zeros + marker_pair + shifting_block + trailing_elements
    
    # Return the newly constructed sequence
    return output_sequence