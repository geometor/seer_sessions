"""
Identify the single row of the input grid. Locate the first contiguous sequence (segment) of non-white pixels (values > 0) within that row. If found, determine the most frequent color (dominant color) within that segment. Create a copy of the input grid and modify it by replacing all pixels within the identified segment's column range in the first row with the dominant color. If no non-white segment is found, return the original grid unchanged.
"""

import numpy as np
import collections

def find_first_non_white_segment(row):
    """
    Finds the start and end indices of the first contiguous non-white segment in a 1D array.

    Args:
        row (np.array): A 1D numpy array representing a row of the grid.

    Returns:
        tuple: (start_index, end_index) or (None, None) if no segment found.
               end_index is inclusive.
    """
    start_index = None
    end_index = None
    n = len(row)

    for i, pixel in enumerate(row):
        # Found the start of the first segment
        if pixel != 0 and start_index is None:
            start_index = i
        # Found the end of the segment (transition back to white or end of array)
        elif start_index is not None:
            if pixel == 0:
                end_index = i - 1
                break # Stop after finding the first segment
            elif i == n - 1: # Reached the end while in a segment
                end_index = i
                break

    return start_index, end_index

def find_dominant_color(segment):
    """
    Finds the most frequent color in a segment (1D array or list).

    Args:
        segment (np.array or list): The segment of the array (pixel values).

    Returns:
        int: The dominant color value. Returns None if segment is empty or invalid.
    """
    if segment is None or len(segment) == 0:
        return None
    # Count occurrences of each color
    counts = collections.Counter(segment)
    # Find the color with the maximum count. most_common(1) returns a list like [ (color, count) ]
    if not counts: # Handle case of empty segment after potential slicing errors
        return None
    dominant_color = counts.most_common(1)[0][0]
    return dominant_color

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.
                                  Assumed to be 1xN for this specific task based on examples.

    Returns:
        np.ndarray: A new 2D numpy array representing the transformed output grid.
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)

    # Check if the grid has at least one row
    if input_grid.shape[0] == 0:
        return output_grid # Return copy of empty grid

    # Extract the first row (assuming 1xN structure as seen in examples)
    # If the grid could be MxN, logic would need adaptation (e.g., iterate rows)
    row = input_grid[0, :]

    # Find the first contiguous non-white segment in the row
    start, end = find_first_non_white_segment(row)

    # If no segment is found, return the original grid copy
    if start is None:
        return output_grid

    # Extract the segment from the row
    # Slicing is exclusive of the end index, so add 1
    segment = row[start : end + 1]

    # Determine the dominant color within the segment
    dominant_color = find_dominant_color(segment)

    # If segment was empty or dominant color couldn't be found (safety check)
    if dominant_color is None:
        return output_grid # Should not happen if start is not None

    # Modify the output grid: replace pixels in the segment range with the dominant color
    # We modify the first row of the output grid in the identified column range
    output_grid[0, start : end + 1] = dominant_color

    # Return the modified grid
    return output_grid