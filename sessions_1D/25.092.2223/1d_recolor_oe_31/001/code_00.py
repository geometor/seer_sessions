"""
Identify contiguous horizontal segments of gray (5) pixels in the input grid.
If the length of a gray segment is odd, replace all its pixels with yellow (4).
If the length of a gray segment is even, replace all its pixels with orange (7).
Leave all white (0) pixels unchanged.
The input is treated as a 1D array or a 1xN grid.
"""

import copy

def find_gray_segments(grid):
    """
    Identifies the start index, end index, and length of contiguous gray (5) segments.

    Args:
        grid: A list of integers representing the 1D grid.

    Returns:
        A list of tuples, where each tuple is (start_index, end_index, length).
    """
    segments = []
    in_segment = False
    start_index = -1
    for i, pixel in enumerate(grid):
        if pixel == 5 and not in_segment:
            # Start of a new segment
            in_segment = True
            start_index = i
        elif pixel != 5 and in_segment:
            # End of the current segment
            in_segment = False
            end_index = i - 1
            length = end_index - start_index + 1
            segments.append((start_index, end_index, length))
            start_index = -1 # Reset start index

    # Check if the grid ends with a segment
    if in_segment:
        end_index = len(grid) - 1
        length = end_index - start_index + 1
        segments.append((start_index, end_index, length))

    return segments

def transform(input_grid):
    """
    Transforms the input grid based on the length parity of gray segments.

    Args:
        input_grid: A list of integers representing the 1D input grid.

    Returns:
        A list of integers representing the transformed 1D output grid.
    """
    # Initialize output_grid as a copy of the input
    # This handles white pixels (0) correctly as they remain unchanged
    output_grid = copy.deepcopy(input_grid)

    # Find all contiguous segments of gray pixels (5)
    gray_segments = find_gray_segments(input_grid)

    # Iterate through the found segments and apply the transformation rules
    for start, end, length in gray_segments:
        # Determine the replacement color based on the length's parity
        if length % 2 != 0:  # Odd length
            replacement_color = 4 # yellow
        else:  # Even length
            replacement_color = 7 # orange

        # Apply the replacement color to the segment in the output grid
        for i in range(start, end + 1):
            output_grid[i] = replacement_color

    return output_grid
