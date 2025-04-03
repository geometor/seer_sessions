"""
Transform a 1D array (list) of color values based on the following rule:
1. Identify the contiguous segment of non-zero (non-white) pixels.
2. Determine the "dominant color", which is the color of the first pixel in this segment.
3. Iterate through the segment. Replace any pixel within the segment that is non-zero and not the dominant color with the dominant color.
4. Leave all zero (white) pixels and pixels already matching the dominant color unchanged.
"""

import numpy as np # Although not strictly needed for lists, it's common in ARC tasks

def find_segment_and_dominant_color(input_list):
    """
    Finds the start and end indices of the first contiguous non-zero segment
    and the dominant color (color of the first element in the segment).

    Args:
        input_list: A list of integers representing colors.

    Returns:
        A tuple (start_index, end_index, dominant_color) if a segment is found,
        otherwise returns (None, None, None).
    """
    start_index = -1
    dominant_color = None

    # Find the start index and dominant color
    for i, val in enumerate(input_list):
        if val != 0:
            start_index = i
            dominant_color = val
            break

    # If no non-zero element found, return None
    if start_index == -1:
        return None, None, None

    end_index = start_index
    # Find the end index by searching backwards from the end
    # Note: This assumes only ONE contiguous segment of non-zeros surrounded by zeros.
    # A more robust approach might be needed if multiple segments could exist,
    # but based on examples, this seems sufficient.
    for i in range(len(input_list) - 1, start_index - 1, -1):
         if input_list[i] != 0:
             end_index = i
             break # Found the last non-zero element

    return start_index, end_index, dominant_color


def transform(input_grid: list) -> list:
    """
    Transforms the input list by homogenizing the color of the central non-zero segment
    to match the color of its first element.

    Args:
        input_grid: A list of integers representing colors.

    Returns:
        A new list with the transformation applied.
    """

    # Find the non-zero segment boundaries and the dominant color
    start_index, end_index, dominant_color = find_segment_and_dominant_color(input_grid)

    # If no segment is found (e.g., all zeros), return a copy of the input
    if start_index is None:
        return input_grid[:]

    # Initialize the output grid as a copy of the input grid
    output_grid = input_grid[:]

    # Iterate through the identified segment
    for i in range(start_index, end_index + 1):
        # Check if the current pixel is within the segment (non-zero)
        # and if its color is different from the dominant color
        if output_grid[i] != 0 and output_grid[i] != dominant_color:
            # If it's an 'impurity', change its color to the dominant color
            output_grid[i] = dominant_color

    # Return the modified grid
    return output_grid