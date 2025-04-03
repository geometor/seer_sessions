"""
Transformation Rule:

1. Identify the contiguous segment of non-white pixels (value > 0) within the input 1D array (row).
2. If no non-white pixels exist, return the input array unchanged.
3. Within this non-white segment, determine the most frequent non-white color (the "dominant color").
4. Create an output array by copying the input array.
5. Iterate through the non-white segment in the output array and replace all pixels that are *not* the dominant color with the dominant color.
6. Leave white pixels (value 0) and pixels already matching the dominant color unchanged.
"""

import numpy as np
from collections import Counter
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(message)s')

def find_non_white_segment(arr):
    """Finds the start and end indices of the contiguous non-white segment."""
    non_white_indices = np.where(arr != 0)[0]
    if len(non_white_indices) == 0:
        # No non-white pixels found
        return None, None, None
    
    start_index = non_white_indices[0]
    end_index = non_white_indices[-1]
    segment = arr[start_index:end_index+1]
    
    # Verify contiguity (optional but good check)
    # Check if all pixels between start and end are non-zero
    # This assumption holds in the examples, but might not always
    # if np.any(arr[start_index:end_index+1] == 0):
    #     logging.warning("Non-white segment is not contiguous based on start/end indices. Processing assumes it is.")
         # Or handle more complex cases if needed

    return start_index, end_index, segment

def find_dominant_color(segment):
    """Finds the most frequent non-white color in a segment."""
    if segment is None or len(segment) == 0:
        return None

    # Filter out any potential zeros if the segment definition was loose
    non_white_pixels = segment[segment != 0]
    
    if len(non_white_pixels) == 0:
        # Segment exists but contains only zeros (shouldn't happen with find_non_white_segment)
        return None

    # Count occurrences of each non-white color
    color_counts = Counter(non_white_pixels)
    
    # Find the color with the maximum count
    dominant_color = color_counts.most_common(1)[0][0]
    # logging.info(f"Segment: {segment}, Counts: {color_counts}, Dominant: {dominant_color}")
    return dominant_color

def transform(input_grid):
    """
    Applies the homogenization transformation to a single row (1D numpy array).

    Args:
        input_grid (np.array): A 1D numpy array representing a row of pixels.

    Returns:
        np.array: The transformed 1D numpy array.
    """
    # Ensure input is a numpy array
    if not isinstance(input_grid, np.ndarray):
        input_grid = np.array(input_grid)
        
    if input_grid.ndim != 1:
        raise ValueError(f"Input must be a 1D array, but got shape {input_grid.shape}")

    # Initialize output_grid as a copy of the input
    output_grid = input_grid.copy()

    # 1. Identify the non-white segment
    start_idx, end_idx, segment = find_non_white_segment(output_grid)

    # 2. If no non-white segment, return the original grid
    if start_idx is None:
        # logging.info("No non-white segment found. Returning original grid.")
        return output_grid

    # 3. Determine the dominant color within the segment
    dominant_color = find_dominant_color(segment)

    # If segment exists but somehow no dominant color found (e.g., only zeros)
    if dominant_color is None:
         # logging.warning("Non-white segment identified, but no dominant color found (maybe only zeros?). Returning original grid.")
         return output_grid # Should not happen with current logic but safe fallback

    # 4. & 5. Iterate through the segment and replace non-dominant colors
    # logging.info(f"Processing segment from index {start_idx} to {end_idx}. Dominant color: {dominant_color}")
    for i in range(start_idx, end_idx + 1):
        # Check if the current pixel is non-white and not the dominant color
        if output_grid[i] != 0 and output_grid[i] != dominant_color:
            # logging.info(f"Changing pixel at index {i} from {output_grid[i]} to {dominant_color}")
            output_grid[i] = dominant_color
            
    # 6. White pixels and dominant color pixels are already handled (left unchanged)
    return output_grid
