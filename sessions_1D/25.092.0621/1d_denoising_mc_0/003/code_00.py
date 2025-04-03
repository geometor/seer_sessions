"""
Examine the input 1D array of pixels.
Find the starting index and ending index of the first continuous sequence of non-white (color not 0) pixels.
If no non-white pixels are found, return a copy of the input array.
If a non-white sequence is found, identify all the pixels within this sequence (from the start index to the end index, inclusive).
Count the occurrences of each color within this identified sequence.
Determine the color that occurs most frequently (the dominant color). In case of a tie, select any one of the most frequent colors.
Create a new array identical to the input array.
Modify the new array: replace all pixels within the identified sequence (from the start index to the end index) with the determined dominant color.
Return the modified array.
"""

import collections
import numpy as np # Using numpy for potential array operations, but core logic uses lists

def find_first_non_white_segment(input_array):
    """
    Finds the start and end indices of the first contiguous non-white segment.

    Args:
        input_array (list): The 1D input array.

    Returns:
        tuple: (start_index, end_index) or (None, None) if no segment found.
               end_index is inclusive.
    """
    start_index = None
    end_index = None
    n = len(input_array)

    for i, pixel in enumerate(input_array):
        # Found the start of the first segment
        if pixel != 0 and start_index is None:
            start_index = i
        # Found the end of the segment (transition back to white)
        elif pixel == 0 and start_index is not None:
            end_index = i - 1
            break # Stop after finding the first segment
        # Check if the segment runs to the very end of the array
        elif start_index is not None and i == n - 1:
             end_index = i
             break # Reached the end while in a segment

    # Handle case where the entire array is non-white (start found, no end triggered)
    # This check is redundant due to the i == n-1 check above, but kept for clarity
    # if start_index is not None and end_index is None:
    #     end_index = n - 1

    return start_index, end_index

def find_dominant_color(segment):
    """
    Finds the most frequent color in a segment.

    Args:
        segment (list): The segment of the array (list of pixel values).

    Returns:
        int: The dominant color value. Returns None if segment is empty.
    """
    if not segment:
        return None
    # Count occurrences of each color
    counts = collections.Counter(segment)
    # Find the color with the maximum count. most_common(1) returns a list like [ (color, count) ]
    dominant_color = counts.most_common(1)[0][0]
    return dominant_color

def transform(input_grid):
    """
    Applies the transformation rule to the input grid (1D array).

    Args:
        input_grid (list or np.array): A 1D list/array representing the input.

    Returns:
        list: A new 1D list representing the transformed output array.
    """
    # Ensure input is a list for consistent processing
    input_list = list(input_grid)

    # Initialize output_grid as a copy of the input
    output_grid = list(input_list)

    # 1. Find the first contiguous non-white segment
    start, end = find_first_non_white_segment(input_list)

    # 2. If no segment is found, return the original grid copy
    if start is None:
        return output_grid

    # 3. Extract the segment
    # Note: Python slicing is exclusive of the end index, so add 1
    segment = input_list[start : end + 1]

    # 4. Determine the dominant color within the segment
    dominant_color = find_dominant_color(segment)

    # Should not happen if start is not None, but safety check
    if dominant_color is None:
        return output_grid

    # 5. Modify the output grid: replace pixels in the segment range with the dominant color
    for i in range(start, end + 1):
        output_grid[i] = dominant_color

    # 6. Return the modified grid
    return output_grid