import numpy as np
from typing import List, Tuple

"""
Transforms the input grid by operating on its single row. It identifies contiguous
horizontal segments of red (2) pixels. Each identified red segment is then recolored
based on its length:
- Segments of length 1 are changed to blue (1).
- Segments of length 2 are changed to azure (8).
- Segments of length 3 are changed to gray (5).
Pixels that were originally white (0) and not part of a red segment remain unchanged.
The output is a 2D grid containing the single transformed row.
"""


def find_contiguous_segments(row: List[int], target_color: int) -> List[Tuple[int, int]]:
    """
    Identifies contiguous horizontal segments of a specific target color in a row.

    Args:
        row (List[int]): A single row (list of integers) from the grid.
        target_color (int): The color value of the segments to find.

    Returns:
        List[Tuple[int, int]]: A list of tuples, where each tuple contains
                               (start_index, length) of a found segment.
    """
    segments = []
    start_index = -1
    current_length = 0
    # Iterate through the row with index
    for i, pixel in enumerate(row):
        # Check if the current pixel matches the target color
        if pixel == target_color:
            # If this is the start of a new segment, record the start index
            if start_index == -1:
                start_index = i
            # Increment the length of the current segment
            current_length += 1
        else:
            # If we were tracking a segment, it has now ended
            if start_index != -1:
                # Add the found segment (start index, length) to the list
                segments.append((start_index, current_length))
                # Reset tracking variables
                start_index = -1
                current_length = 0
    # After the loop, check if a segment was ongoing until the end of the row
    if start_index != -1:
        segments.append((start_index, current_length))
    return segments

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (List[List[int]]): A 2D list representing the input grid,
                                     expected to contain a single row.

    Returns:
        List[List[int]]: A 2D list representing the transformed grid,
                         containing the single modified row.
    """
    # Handle empty or incorrectly structured input
    if not input_grid or not input_grid[0]:
        return input_grid # Return unchanged if input is empty

    # Extract the single row from the 2D input grid
    input_row = input_grid[0]

    # Initialize the output row as a mutable copy of the input row
    # This ensures background pixels (0) are preserved by default
    output_row = list(input_row)

    # Define the mapping from red segment length to the corresponding output color
    length_to_color_map = {
        1: 1,  # Length 1 -> Blue
        2: 8,  # Length 2 -> Azure
        3: 5   # Length 3 -> Gray
    }

    # Find all contiguous segments of red (color 2) pixels in the input row
    red_segments = find_contiguous_segments(input_row, 2)

    # Iterate through each identified red segment
    for start_index, length in red_segments:
        # Determine the new color based on the segment's length using the map
        output_color = length_to_color_map.get(length)

        # Check if the length has a corresponding mapping (1, 2, or 3)
        if output_color is not None:
            # Recolor the pixels within this segment's range in the output row
            for i in range(start_index, start_index + length):
                output_row[i] = output_color
        # If length is not in the map (e.g., 4+), the original red pixels remain
        # unchanged in the output_row because they were copied initially.

    # Wrap the modified row in a list to return it as a 2D grid format
    output_grid = [output_row]
    return output_grid