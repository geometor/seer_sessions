import numpy as np
from typing import List, Tuple

"""
Change the color of the longest horizontal segment(s) of maroon (9) pixels 
in the input sequence to yellow (4). If multiple segments share the maximum 
length, change all of them. Treat the input as a 1D sequence.
"""

def find_maroon_segments(sequence: List[int]) -> List[Tuple[int, int, int]]:
    """
    Identifies contiguous segments of maroon (9) pixels in a 1D sequence.

    Args:
        sequence: A list of integers representing pixel colors.

    Returns:
        A list of tuples, where each tuple represents a maroon segment
        and contains (start_index, end_index, length).
    """
    segments = []
    start_index = -1
    current_length = 0
    maroon_color = 9

    for i, pixel in enumerate(sequence):
        if pixel == maroon_color:
            if start_index == -1:
                start_index = i
            current_length += 1
        else:
            if start_index != -1:
                # End of a segment
                segments.append((start_index, i - 1, current_length))
                start_index = -1
                current_length = 0

    # Handle segment ending at the very end of the sequence
    if start_index != -1:
        segments.append((start_index, len(sequence) - 1, current_length))

    return segments

def transform(input_grid: List[int]) -> List[int]:
    """
    Applies the transformation rule to a 1D input sequence.

    Args:
        input_grid: A list of integers representing the input pixel sequence.

    Returns:
        A list of integers representing the transformed pixel sequence.
    """
    # Treat the input as a 1D sequence
    sequence = input_grid

    # Initialize output_grid as a copy of the input
    output_grid = list(sequence)
    
    # --- Identify maroon segments ---
    maroon_segments = find_maroon_segments(sequence)

    # --- Handle case with no maroon segments ---
    if not maroon_segments:
        return output_grid # Return the original sequence if no maroon found

    # --- Find the maximum length among the segments ---
    max_length = 0
    for _, _, length in maroon_segments:
        if length > max_length:
            max_length = length

    # --- Recolor the longest segments ---
    yellow_color = 4
    for start, end, length in maroon_segments:
        if length == max_length:
            # Change the color of pixels in this segment to yellow in the output
            for i in range(start, end + 1):
                output_grid[i] = yellow_color

    return output_grid