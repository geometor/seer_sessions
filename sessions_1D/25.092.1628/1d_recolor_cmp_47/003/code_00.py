import numpy as np
from typing import List, Tuple

"""
Treat the input grid as a one-dimensional array of pixels.
Scan the input array to identify all distinct contiguous segments composed solely of gray (5) pixels. Record the start index, end index, and length for each segment.
If no gray segments are found, the output is identical to the input.
If gray segments are found, determine the maximum length (`max_len`) among all the identified segments.
Create the output array, initially identical to the input array.
Iterate through each identified gray segment.
If a segment's length is equal to `max_len`, change the color of all pixels within that segment in the output array from gray (5) to azure (8).
Segments with length less than `max_len` retain their gray (5) color. White (0) pixels remain unchanged.
Return the modified array as the output.
"""

GRAY = 5
AZURE = 8

def find_contiguous_segments(grid_row: np.ndarray, target_color: int) -> List[Tuple[Tuple[int, int], int]]:
    """
    Finds contiguous horizontal segments of a target color in a 1D numpy array.

    Args:
        grid_row: A 1D numpy array of integers representing a row or flattened grid.
        target_color: The integer color value to find segments of.

    Returns:
        A list of tuples, where each tuple represents a segment
        and contains ((start_index, end_index), length). End_index is inclusive.
        Returns an empty list if no segments are found.
    """
    segments = []
    start_index = -1
    n = len(grid_row)
    for i, pixel in enumerate(grid_row):
        if pixel == target_color and start_index == -1:
            # Start of a new segment
            start_index = i
        elif pixel != target_color and start_index != -1:
            # End of the current segment (exclusive index is i)
            end_index = i - 1
            length = end_index - start_index + 1
            segments.append(((start_index, end_index), length))
            start_index = -1 # Reset for next potential segment
            
    # Check if the last segment extends to the end of the row
    if start_index != -1:
        end_index = n - 1
        length = end_index - start_index + 1
        segments.append(((start_index, end_index), length))
        
    return segments

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid by changing the color of the longest gray segments.
    Assumes input_grid is a 1D numpy array.

    Args:
        input_grid: A 1D numpy array representing the input grid.

    Returns:
        A 1D numpy array representing the transformed output grid.
    """
    # Ensure input is treated as 1D
    if input_grid.ndim > 1:
        # If input is somehow 2D+, flatten it. Based on analysis, it should be 1D.
        input_1d = input_grid.flatten()
    else:
        input_1d = input_grid

    # Find all contiguous segments of gray pixels
    gray_segments = find_contiguous_segments(input_1d, GRAY)

    # If no gray segments are found, return the input grid as is
    if not gray_segments:
        return input_1d.copy()

    # Calculate the lengths and find the maximum length
    segment_lengths = [length for _, length in gray_segments]
    max_len = max(segment_lengths)

    # Initialize the output grid as a copy of the input grid
    output_grid = input_1d.copy()

    # Iterate through the identified gray segments
    for segment_info, length in gray_segments:
        start_index, end_index = segment_info
        
        # If the segment's length is equal to the maximum length
        if length == max_len:
            # Change the color of the pixels in this segment to azure
            # Use slicing for efficiency with numpy arrays
            output_grid[start_index : end_index + 1] = AZURE
            
    # Segments with length less than max_len remain gray (already copied)
    # White pixels remain white (already copied)

    return output_grid