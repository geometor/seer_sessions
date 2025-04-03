"""
Identify the contiguous sequence of non-white pixels (primary segment) in the 
single row of the 1xN input grid. Count the occurrences of each non-white 
color within this segment. Determine the dominant color (most frequent 
non-white color). Create the output grid by copying the input. Iterate 
through the primary segment in the output grid's row and replace any 
non-white pixel that is not the dominant color with the dominant color. 
Leave white (0) pixels unchanged.
"""

import numpy as np
from collections import Counter

def find_primary_segment_indices(row_array):
    """Finds the start and end column indices of the non-white segment."""
    non_white_indices = np.where(row_array != 0)[0]
    if len(non_white_indices) == 0:
        return None, None  # No non-white pixels found
    start_col = np.min(non_white_indices)
    end_col = np.max(non_white_indices)
    return start_col, end_col

def find_dominant_color(segment_array):
    """Finds the most frequent non-white color in a segment."""
    # Filter out white pixels (0) before counting
    non_white_pixels = segment_array[segment_array != 0]
    if len(non_white_pixels) == 0:
        return None # No non-white pixels in the segment
        
    color_counts = Counter(non_white_pixels)
    # most_common(1) returns a list like [(color, count)]
    dominant_color = color_counts.most_common(1)[0][0]
    return dominant_color

def transform(input_grid):
    """
    Transforms the input grid by replacing non-dominant colors in the primary
    segment with the dominant color.

    Args:
        input_grid (list): A list containing a single list representing the 1xN grid.

    Returns:
        list: The transformed grid in the same list-of-lists format.
    """
    # Convert input list-of-lists to a NumPy array
    input_array = np.array(input_grid, dtype=int)

    # Ensure the input is a 1xN grid (or handle other cases if necessary)
    if input_array.shape[0] != 1:
        # For this specific task, we assume 1xN. If not, return input or raise error.
        # Returning input might be safer for ARC if unexpected shapes occur.
        return input_grid 

    # Extract the single row
    row_array = input_array[0]
    
    # Initialize the output array as a copy of the input
    output_array = input_array.copy()
    output_row = output_array[0] # Get a reference to the row to modify

    # Find the start and end indices of the primary segment
    start_col, end_col = find_primary_segment_indices(row_array)

    # If no segment exists (all white), return the original grid
    if start_col is None:
        return output_array.tolist() 

    # Extract the primary segment from the input row
    primary_segment = row_array[start_col : end_col + 1]

    # Determine the dominant color within this segment
    dominant_color = find_dominant_color(primary_segment)

    # If a dominant color was found (i.e., the segment had non-white pixels)
    if dominant_color is not None:
        # Iterate through the columns of the primary segment in the output row
        for i in range(start_col, end_col + 1):
            # Check if the pixel is non-white AND not the dominant color
            if output_row[i] != 0 and output_row[i] != dominant_color:
                # Replace it with the dominant color
                output_row[i] = dominant_color

    # Convert the modified NumPy array back to a list of lists
    return output_array.tolist()