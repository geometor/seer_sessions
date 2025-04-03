"""
Identifies the span containing all non-white pixels (from the index of the 
first non-white pixel to the index of the last non-white pixel) in a 1D input 
array (list). Within this span, it determines the most frequent non-white 
color (mode). It then creates a new array where all pixels within this span 
are replaced by the mode color, while pixels outside the span remain unchanged 
from the input.
"""

import numpy as np
from collections import Counter

def find_non_white_span_indices(arr):
    """
    Finds the start and end indices of the span covering all non-white pixels.
    The span starts at the minimum index of a non-white pixel and ends at the
    maximum index of a non-white pixel.

    Args:
        arr: A numpy array representing the input grid row.

    Returns:
        A tuple (start_index, end_index). Returns (None, None) if no 
        non-white pixels are found.
    """
    # Find indices of all elements that are not 0 (non-white)
    non_white_indices = np.where(arr != 0)[0]
    
    # If no non-white pixels are found, return None for indices
    if len(non_white_indices) == 0:
        return None, None
        
    # Determine the minimum and maximum index among non-white pixels
    start_index = np.min(non_white_indices)
    end_index = np.max(non_white_indices)
    
    return start_index, end_index

def find_dominant_color_in_span(arr_slice):
    """
    Finds the most frequent non-white color (mode) in a given array slice.

    Args:
        arr_slice: A numpy array slice representing the span.

    Returns:
        The most frequent non-white color value. Returns None if the slice 
        is empty or contains only white pixels.
    """
    # Filter out white (0) pixels from the slice
    non_white_pixels = arr_slice[arr_slice != 0]
    
    # If there are no non-white pixels in the slice, return None
    if len(non_white_pixels) == 0:
        # This case should ideally not happen if the span is correctly identified
        # based on find_non_white_span_indices, unless the input was unusual.
        # However, handling it defensively. If the span truly contains only zeros,
        # there's no non-white dominant color. The original NL description implies
        # the span is defined *by* non-white pixels, so this path might indicate
        # an issue upstream or a misunderstanding of an edge case.
        # Based on examples, a non-white span will always contain non-white pixels.
        return None 
        
    # Count the frequency of each non-white color
    counts = Counter(non_white_pixels)
    
    # Determine the mode (most frequent color)
    # most_common(1) returns a list like [(color, count)], we extract the color
    dominant_color = counts.most_common(1)[0][0]
    
    return dominant_color

def transform(input_grid):
    """
    Transforms the input 1D grid according to the rule: homogenize the color
    within the span of non-white pixels based on the most frequent non-white color.

    Args:
        input_grid: A list of integers representing the input 1D grid.

    Returns:
        A list of integers representing the transformed 1D grid.
    """
    # Convert input list to a numpy array for efficient processing
    input_arr = np.array(input_grid, dtype=int)
    
    # Handle empty input grid
    if input_arr.size == 0:
        return []

    # Step 1 & 2: Find the start and end indices of the non-white span
    start_index, end_index = find_non_white_span_indices(input_arr)

    # Step 3: If no non-white pixels exist, return the original grid unchanged
    if start_index is None:
        return input_grid # Return original list format

    # Step 4 & 5: Extract the sub-array (slice) corresponding to the span
    # Numpy slicing is exclusive of the end index, so add 1 to include end_index
    span_slice = input_arr[start_index : end_index + 1]

    # Step 6 & 7: Determine the dominant (most frequent) non-white color in the slice
    dominant_color = find_dominant_color_in_span(span_slice)
    
    # Handle potential edge case where dominant color couldn't be found (e.g., only zeros in span)
    # Though, this shouldn't happen with the current logic of finding the span.
    if dominant_color is None:
         # If the span exists but has no non-white pixels (contradictory?), return original.
         # Or, perhaps fill with 0? The task seems focused on non-white homogenization.
         # Let's assume returning original is safest if this unexpected state occurs.
         return input_grid 

    # Step 8: Create a copy of the input array to modify
    output_arr = input_arr.copy()

    # Step 9: Modify the copied array: replace all elements within the span
    # (from start_index to end_index inclusive) with the dominant color.
    output_arr[start_index : end_index + 1] = dominant_color

    # Step 10: Return the modified array converted back to a list
    return output_arr.tolist()