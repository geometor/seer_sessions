"""
Transforms an input row by identifying the contiguous segment of non-white pixels,
determining the most frequent non-white color (dominant color) within that segment,
and then changing any non-white pixel within the segment that is not the dominant
color to become the dominant color. White pixels and pixels already matching the
dominant color remain unchanged.
"""

import numpy as np
from collections import Counter
import copy

def find_non_white_segment_indices(row):
    """
    Finds the start and end indices of the segment containing all non-white pixels.
    Args:
        row (np.array): A 1D numpy array representing a row of pixels.
    Returns:
        tuple: (start_index, end_index) or (None, None) if no non-white pixels.
    """
    non_white_indices = np.where(row != 0)[0]
    if len(non_white_indices) == 0:
        return None, None  # No non-white pixels found
    start_index = non_white_indices[0]
    end_index = non_white_indices[-1]
    return start_index, end_index

def find_dominant_color(segment):
    """
    Finds the most frequent non-white color in a segment.
    Args:
        segment (np.array): A 1D numpy array representing the segment of interest.
    Returns:
        int: The dominant non-white color, or None if the segment has no non-white pixels.
    """
    non_white_pixels = segment[segment != 0]
    if len(non_white_pixels) == 0:
        return None
    
    # Count frequencies of non-white colors
    counts = Counter(non_white_pixels)
    
    # Find the color with the maximum count. If there's a tie, Counter.most_common picks one.
    dominant_color = counts.most_common(1)[0][0]
    return dominant_color

def transform(input_grid):
    """
    Applies the transformation rule to the input grid. Assumes the grid contains one row.
    
    Args:
        input_grid (list or np.array): A 1D list or numpy array representing the input row.
                                        If 2D, assumes it's a 1xN grid.
    
    Returns:
        np.array: The transformed 1D numpy array.
    """
    # Ensure input is a numpy array and handle potential 2D shape (1xN)
    input_array = np.array(input_grid)
    if input_array.ndim > 1:
      if input_array.shape[0] == 1:
         input_row = input_array[0] # Extract the single row
      elif input_array.shape[1] == 1:
         input_row = input_array.flatten() # Treat as a row if it's Nx1
      else:
          # If truly 2D with multiple rows, this rule doesn't fit.
          # Based on examples, assume it's effectively 1D.
          # We'll process the first row if ambiguous, but ideally input matches examples.
          # For safety, let's just focus on the first row if multiple exist.
          input_row = input_array[0] 
    else:
        input_row = input_array

    # Initialize output_row as a copy of the input row
    output_row = input_row.copy()

    # Find the segment containing non-white pixels
    start_index, end_index = find_non_white_segment_indices(input_row)

    # If no non-white pixels, return the original row
    if start_index is None:
        return output_row.tolist() # Return as list, standard ARC format

    # Extract the segment from the start to the end index (inclusive)
    # Note: We need the actual segment from the *original* row for frequency analysis
    segment_for_analysis = input_row[start_index : end_index + 1]

    # Find the dominant color within this segment
    dominant_color = find_dominant_color(segment_for_analysis)

    # If a dominant color was found (i.e., segment wasn't all white)
    if dominant_color is not None:
        # Iterate through the segment indices in the output row
        for i in range(start_index, end_index + 1):
            # If the pixel is non-white and not the dominant color, change it
            if output_row[i] != 0 and output_row[i] != dominant_color:
                output_row[i] = dominant_color

    # Return the modified row as a list
    return output_row.tolist()