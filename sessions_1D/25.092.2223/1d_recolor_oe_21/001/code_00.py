import numpy as np
from typing import List, Tuple

"""
Recolors contiguous horizontal sequences of red (2) pixels based on their order of appearance from left to right.

1. Identifies all contiguous horizontal sequences (blocks) of red (2) pixels.
2. Iterates through these sequences from left to right.
3. Recolors the first, third, fifth, etc. (odd-indexed based on 1-counting) red sequence to blue (1).
4. Recolors the second, fourth, sixth, etc. (even-indexed based on 1-counting) red sequence to orange (7).
5. Leaves all other pixels (specifically white/0) unchanged.
"""

def find_sequences(row: List[int], target_color: int) -> List[Tuple[int, int]]:
    """
    Finds contiguous sequences of a target color in a 1D list.

    Args:
        row: The input list of integers (pixels).
        target_color: The color value to find sequences of.

    Returns:
        A list of tuples, where each tuple contains the start and end
        index (inclusive) of a sequence.
    """
    sequences = []
    start_index = -1
    for i, pixel in enumerate(row):
        if pixel == target_color and start_index == -1:
            # Start of a new sequence
            start_index = i
        elif pixel != target_color and start_index != -1:
            # End of the current sequence
            sequences.append((start_index, i - 1))
            start_index = -1
    # Check if the row ends with a sequence
    if start_index != -1:
        sequences.append((start_index, len(row) - 1))
    return sequences

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the alternating recoloring transformation to the input grid (assumed 1xN).

    Args:
        input_grid: A list containing a single list representing the input row.

    Returns:
        A list containing a single list representing the transformed output row.
    """
    # Since the input examples are 1xN, we work with the first row.
    # Use np.array for easier slicing and modification, then convert back.
    input_row = np.array(input_grid[0])
    output_row = input_row.copy()

    # Define colors
    red_color = 2
    blue_color = 1
    orange_color = 7

    # Find all sequences of the red color
    red_sequences = find_sequences(input_row.tolist(), red_color)

    # Iterate through the found sequences and apply alternating colors
    for i, (start, end) in enumerate(red_sequences):
        # Determine the target color based on sequence index (0-based)
        # Odd sequence (1st, 3rd, ...) -> index 0, 2, ... -> blue
        # Even sequence (2nd, 4th, ...) -> index 1, 3, ... -> orange
        if i % 2 == 0:  # Odd sequence (1st, 3rd, etc.)
            target_color = blue_color
        else:  # Even sequence (2nd, 4th, etc.)
            target_color = orange_color

        # Recolor the segment in the output row
        output_row[start : end + 1] = target_color

    # Convert the result back to the required list-of-lists format
    return [output_row.tolist()]
