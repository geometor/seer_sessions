import numpy as np
from collections import Counter
import copy

"""
Transforms a single-row grid by identifying the contiguous segment of non-white 
pixels (pixels with value > 0). It then determines the most frequent color 
within that segment (dominant color), handling ties by choosing the color that 
appears first in the segment among those with the highest frequency. Finally, it 
replaces all pixels within that segment's original index range in the output grid 
with the determined dominant color. Pixels outside this segment (typically 
white background pixels with value 0) remain unchanged.
"""

def find_non_white_segment_1d(grid_row):
    """
    Finds the start and end column indices of the contiguous non-white segment in a 1D row.

    Args:
        grid_row (np.array): A 1D numpy array representing a row of pixels.

    Returns:
        tuple: (start_index, end_index) if a segment is found, otherwise (None, None).
    """
    # Find indices of all non-zero elements
    non_white_indices = np.where(grid_row != 0)[0]
    
    # If no non-zero elements, return None
    if len(non_white_indices) == 0:
        return None, None 

    # Determine the start and end of the segment based on min and max indices
    # This inherently handles contiguity as defined by the problem examples
    start_index = np.min(non_white_indices)
    end_index = np.max(non_white_indices)

    # Return indices as standard Python ints
    return int(start_index), int(end_index) 

def find_dominant_color_segment(segment):
    """
    Finds the most frequent color in a given segment (list or array).
    Handles ties by returning the first encountered color with the maximum frequency 
    in the original segment order.

    Args:
        segment (list or np.array): The pixels within the segment.

    Returns:
        int: The dominant color. Returns 0 if the segment is empty.
    """
    # Ensure segment is a list for consistent processing
    if not isinstance(segment, list):
        segment = list(segment) 

    # Handle empty segment case
    if not segment:
        return 0 

    # Count frequencies of each color
    color_counts = Counter(segment)

    # Find the maximum frequency count among all colors present
    max_count = 0
    if color_counts: # Check if counter is not empty
      max_count = max(color_counts.values())
    else: # Should not happen if segment is not empty, but good for robustness
        return segment[0] if segment else 0 # Return first element or 0 if truly empty

    # Iterate through the original segment to find the first color that has the max count
    dominant_color = segment[0] # Default guess / handles segment with one element
    for color in segment:
        if color_counts[color] == max_count:
            dominant_color = color
            break # Stop as soon as the first dominant color is found

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
    # Ensure input is roughly the expected format (list of lists)
    if not isinstance(input_grid, list) or not input_grid or not isinstance(input_grid[0], list):
        # Return a copy for safety in case of unexpected input format
        return copy.deepcopy(input_grid) 

    # Make a deep copy to avoid modifying the original input list
    output_grid = copy.deepcopy(input_grid)
    
    # Extract the first (and assumed only) row as a numpy array for easier processing
    try:
        # Use the original input grid to define the segment and find dominant color
        grid_row_np_original = np.array(input_grid[0], dtype=int) 
    except IndexError:
         # Handle empty input grid case
         return output_grid # Return the empty list copy [] or [[]]

    # --- Identify Segment ---
    # Find the start and end indices of the non-white segment in the original row
    start_index, end_index = find_non_white_segment_1d(grid_row_np_original)

    # If no segment found, return the unchanged copy of the input
    if start_index is None:
        return output_grid

    # --- Analyze Segment ---
    # Extract the segment pixels from the original input row
    # Segment includes pixels from start_index to end_index (inclusive)
    segment_pixels = grid_row_np_original[start_index : end_index + 1]

    # Find the dominant color in the extracted segment
    dominant_color = find_dominant_color_segment(segment_pixels)

    # --- Modify Output Grid ---
    # Access the row to be modified in the copied output_grid
    output_row = output_grid[0] # This is a list

    # Iterate through the segment indices and replace colors in the output row
    # with the determined dominant color
    for i in range(start_index, end_index + 1):
         # Ensure index is within bounds (should be, but safe check)
         if i < len(output_row):
            output_row[i] = dominant_color
         
    # output_grid[0] has now been updated

    # Return the modified grid (still as List[List[int]])
    return output_grid