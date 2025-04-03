import numpy as np
from collections import Counter
import copy

"""
Transforms a single-row grid by identifying the contiguous segment of non-white 
pixels, finding the most frequent color within that segment, and then replacing 
all pixels in that segment's original location with the dominant color. Pixels 
outside the segment (typically white background pixels) remain unchanged.
"""

def find_non_white_segment_1d(grid_row):
    """
    Finds the start and end column indices of the contiguous non-white segment in a 1D row.

    Args:
        grid_row (np.array): A 1D numpy array representing a row of pixels.

    Returns:
        tuple: (start_index, end_index) if a segment is found, otherwise (None, None).
    """
    non_white_indices = np.where(grid_row != 0)[0]
    if len(non_white_indices) == 0:
        return None, None # No non-white pixels found

    # Although examples show contiguity, we rely on min/max to define the segment bounds
    start_index = np.min(non_white_indices)
    end_index = np.max(non_white_indices)

    return int(start_index), int(end_index) # Convert from numpy int types

def find_dominant_color_segment(segment):
    """
    Finds the most frequent color in a given segment (list or array).
    Handles ties by returning the first encountered color with the maximum frequency.

    Args:
        segment (list or np.array): The pixels within the segment.

    Returns:
        int: The dominant color. Returns 0 if the segment is empty (shouldn't happen in valid cases).
    """
    if not isinstance(segment, list):
        segment = list(segment) # Ensure it's iterable list for Counter and index check

    if not segment:
        return 0 # Default for empty segment

    color_counts = Counter(segment)

    # Find the maximum frequency count
    max_count = 0
    for color in color_counts:
        if color_counts[color] > max_count:
            max_count = color_counts[color]

    # Find the first color in the original segment order that has the max count
    dominant_color = segment[0] # Default guess
    for color in segment:
        if color_counts[color] == max_count:
            dominant_color = color
            break # Found the first one with max count

    return dominant_color

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list): A list containing a single list of integers (the grid row).
                           Example: [[0, 7, 7, 1, 7, 0]]

    Returns:
        list: A list containing the single transformed grid row.
              Example: [[0, 7, 7, 7, 7, 0]]
    """
    # --- Input Validation and Setup ---
    # Ensure input is in the expected format (list of lists)
    if not isinstance(input_grid, list) or not input_grid or not isinstance(input_grid[0], list):
        # Handle invalid input format if necessary, here we might assume valid input based on ARC context
        # For robustness, could raise an error or return input unchanged
        print("Warning: Invalid input format. Expected List[List[int]].")
        return copy.deepcopy(input_grid) # Return a copy to avoid modifying original

    # Make a deep copy to avoid modifying the original input list
    output_grid = copy.deepcopy(input_grid)
    
    # Extract the first (and assumed only) row as a numpy array
    try:
        grid_row_np = np.array(output_grid[0], dtype=int)
    except IndexError:
         print("Warning: Input grid is empty.")
         return output_grid # Return the empty list copy

    # --- Identify Segment ---
    # Find the start and end indices of the non-white segment in the row
    start_index, end_index = find_non_white_segment_1d(grid_row_np)

    # If no segment found, return the unchanged copy of the input
    if start_index is None:
        return output_grid

    # --- Analyze Segment ---
    # Extract the segment pixels from the original row (use grid_row_np for extraction)
    # Segment includes pixels from start_index to end_index (inclusive)
    segment_pixels = grid_row_np[start_index : end_index + 1]

    # Find the dominant color in the extracted segment
    dominant_color = find_dominant_color_segment(segment_pixels)

    # --- Modify Output Grid ---
    # Create a mutable version of the output row (if not already numpy)
    # We modify the row within the output_grid list directly
    output_row = output_grid[0] # This is a list

    # Iterate through the segment indices and replace colors in the output row
    for i in range(start_index, end_index + 1):
         output_row[i] = dominant_color
         
    # output_grid[0] is already updated as output_row refers to it

    # Return the modified grid (still as List[List[int]])
    return output_grid