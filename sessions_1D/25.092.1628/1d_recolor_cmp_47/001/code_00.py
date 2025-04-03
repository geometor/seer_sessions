import numpy as np
from typing import List, Tuple

"""
Identify all contiguous horizontal segments of gray (5) pixels in the input grid (treated as a 1D array).
Calculate the length of each gray segment.
If gray segments exist, find the minimum length among them.
Create the output grid by copying the input grid.
For each gray segment in the input:
  - If its length is strictly greater than the minimum length found, change the color of the corresponding pixels in the output grid to azure (8).
  - Otherwise (if its length is equal to the minimum length), leave the pixels as gray (5).
White (0) pixels remain unchanged.
If no gray segments are found, the output is identical to the input.
"""

def find_horizontal_segments(grid_row: List[int], target_color: int) -> List[Tuple[int, int]]:
    """
    Finds contiguous horizontal segments of a target color in a 1D list.

    Args:
        grid_row: A list of integers representing a row of the grid.
        target_color: The integer color value to find segments of.

    Returns:
        A list of tuples, where each tuple represents a segment
        and contains (start_index, end_index). End_index is inclusive.
    """
    segments = []
    start_index = -1
    for i, pixel in enumerate(grid_row):
        if pixel == target_color and start_index == -1:
            # Start of a new segment
            start_index = i
        elif pixel != target_color and start_index != -1:
            # End of the current segment
            segments.append((start_index, i - 1))
            start_index = -1
    # Check if the last segment extends to the end of the row
    if start_index != -1:
        segments.append((start_index, len(grid_row) - 1))
    return segments

def transform(input_grid: List[int]) -> List[int]:
    """
    Transforms the input grid based on the lengths of horizontal gray segments.

    Args:
        input_grid: A list of integers representing the 1D input grid.

    Returns:
        A list of integers representing the transformed 1D output grid.
    """
    # Treat the input as a single row (1D array)
    grid_row = input_grid
    gray_color = 5
    azure_color = 8

    # Find all horizontal segments of gray pixels
    gray_segments = find_horizontal_segments(grid_row, gray_color)

    # If no gray segments are found, return the input grid as is
    if not gray_segments:
        return list(grid_row) # Return a copy

    # Calculate the lengths of all gray segments
    segment_lengths = [(end - start + 1) for start, end in gray_segments]

    # Find the minimum length among the gray segments
    min_len = min(segment_lengths)

    # Initialize the output grid as a copy of the input grid
    # Use a list for direct modification
    output_grid = list(grid_row)

    # Iterate through the identified gray segments and their lengths
    for i, (start, end) in enumerate(gray_segments):
        length = segment_lengths[i]
        # If the segment's length is greater than the minimum length
        if length > min_len:
            # Change the color of the pixels in this segment to azure
            for j in range(start, end + 1):
                output_grid[j] = azure_color
        # Segments with length equal to min_len remain gray (already copied)
        # White pixels remain white (already copied)

    return output_grid