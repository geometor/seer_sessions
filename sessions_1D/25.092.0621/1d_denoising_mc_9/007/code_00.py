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
    else: 
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
    # Ensure input is roughly the expected format (list of lists with at least one row)
    if not isinstance(input_grid, list) or not input_grid or not isinstance(input_grid[0], list):
        # Return a deep copy for safety in case of unexpected input format
        return copy.deepcopy(input_grid) 

    # Extract the first (and assumed only) row as a numpy array
    try:
        grid_row_np = np.array(input_grid[0], dtype=int) 
    except IndexError:
         # Handle empty input grid row case e.g., [[]]
         return copy.deepcopy(input_grid) 

    # --- Identify Segment ---
    # Find the start and end indices of the non-white segment in the row
    start_index, end_index = find_non_white_segment_1d(grid_row_np)

    # If no segment found, return the input grid unchanged (but as a deep copy)
    if start_index is None:
        return copy.deepcopy(input_grid)

    # --- Analyze Segment ---
    # Extract the segment pixels from the original numpy row
    # Segment includes pixels from start_index to end_index (inclusive)
    segment_pixels = grid_row_np[start_index : end_index + 1]

    # Find the dominant color in the extracted segment
    dominant_color = find_dominant_color_segment(segment_pixels)

    # --- Modify Output Grid ---
    # Create a mutable copy of the original numpy row to modify
    output_row_np = grid_row_np.copy()

    # Replace colors in the copied numpy row within the segment boundaries
    # using numpy slicing for efficiency
    output_row_np[start_index : end_index + 1] = dominant_color
         
    # --- Format Output ---
    # Convert the modified numpy row back to a list
    output_row_list = output_row_np.tolist()

    # Wrap the row list in another list to match the required output format [[...]]
    output_grid = [output_row_list]

    return output_grid