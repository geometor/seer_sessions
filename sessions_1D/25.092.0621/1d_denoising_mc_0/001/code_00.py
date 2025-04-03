import collections
import numpy as np # Although not strictly necessary for 1D, it's common in ARC

"""
Identifies the contiguous block of non-white pixels in a 1D input array.
Determines the most frequent color (dominant color) within this block.
Replaces all pixels within that block with the dominant color, leaving surrounding white pixels unchanged.
"""

def find_non_white_segment(input_array):
    """
    Finds the start and end indices of the first contiguous non-white segment.

    Args:
        input_array (list or np.array): The 1D input array.

    Returns:
        tuple: (start_index, end_index) or (None, None) if no segment found.
               end_index is inclusive.
    """
    start_index = None
    end_index = None
    for i, pixel in enumerate(input_array):
        if pixel != 0 and start_index is None:
            start_index = i
        if pixel == 0 and start_index is not None:
            end_index = i - 1
            break
    # If the segment runs to the end of the array
    if start_index is not None and end_index is None:
         end_index = len(input_array) - 1

    # Handle case where the entire array might be non-white
    if start_index is not None and all(p != 0 for p in input_array[start_index:]):
        end_index = len(input_array) - 1

    return start_index, end_index

def find_dominant_color(segment):
    """
    Finds the most frequent color in a segment.

    Args:
        segment (list or np.array): The segment of the array.

    Returns:
        int: The dominant color value. Returns None if segment is empty.
    """
    if not segment:
        return None
    counts = collections.Counter(segment)
    # Find the color with the maximum count
    dominant_color = counts.most_common(1)[0][0]
    return dominant_color

def transform(input_grid):
    """
    Applies the transformation rule to the input grid (1D array).

    Args:
        input_grid (list): A 1D list representing the input array.

    Returns:
        list: A new 1D list representing the transformed output array.
    """
    # Ensure input is a list if it's passed as numpy array
    input_list = list(input_grid)

    # Initialize output_grid as a copy of the input
    output_grid = list(input_list)

    # 1. Find the contiguous non-white segment
    start, end = find_non_white_segment(input_list)

    # If no non-white segment is found, return the original grid
    if start is None:
        return output_grid

    # 2. Extract the segment
    segment = input_list[start : end + 1]

    # 3. Determine the dominant color within the segment
    dominant_color = find_dominant_color(segment)

    # If the segment was somehow empty or dominant color couldn't be found
    # (shouldn't happen with valid non-white segment), return original.
    if dominant_color is None:
        return output_grid # Or raise an error

    # 4. Modify the output grid: replace pixels in the segment range with the dominant color
    for i in range(start, end + 1):
        output_grid[i] = dominant_color

    # 5. Return the modified grid
    return output_grid