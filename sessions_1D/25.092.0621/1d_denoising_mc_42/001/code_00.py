"""
Identify the contiguous segment of non-white pixels in the input row.
Count the occurrences of each non-white color within this segment.
Determine the color that occurs most frequently (the "dominant color").
Create the output row by replacing all pixels within the identified segment 
with the dominant color. Keep all white (zero) pixels outside the segment 
in their original positions.
"""

import numpy as np
from collections import Counter

def find_non_white_segment(row):
    """
    Finds the start and end indices of the contiguous non-white segment.
    Returns (start_index, end_index) or (None, None) if no segment found.
    """
    non_white_indices = np.where(row != 0)[0]
    if len(non_white_indices) == 0:
        return None, None
    
    start_index = np.min(non_white_indices)
    end_index = np.max(non_white_indices)
    
    # Verify contiguity (although problem description implies it)
    # If the number of non-white pixels isn't equal to the span length,
    # it's not contiguous according to the examples seen.
    # However, the core logic focuses on the span between min and max non-zero.
    # Let's stick to the simpler interpretation for now.
    
    return start_index, end_index

def get_dominant_color(segment):
    """
    Finds the most frequent non-white color in a segment.
    """
    if len(segment) == 0:
        return 0 # Default to white if segment is empty? Or handle upstream.
        
    # Filter out white pixels if any were included (shouldn't be based on find_segment)
    non_white_pixels = segment[segment != 0]
    
    if len(non_white_pixels) == 0:
         # This case might happen if the segment finding included zeros accidentally
         # or if the segment was all zeros (which find_non_white_segment should prevent)
         # Let's return the most frequent color overall in the segment if this happens
         # although it deviates slightly from "most frequent non-white"
        counts = Counter(segment)
        if not counts:
             return 0 # Truly empty or problematic segment
        dominant_color = counts.most_common(1)[0][0]
        return dominant_color

    counts = Counter(non_white_pixels)
    dominant_color = counts.most_common(1)[0][0]
    return dominant_color

def transform(input_grid):
    """
    Transforms the input row according to the dominant color rule.
    """
    # Ensure input is a numpy array (specifically 1D for this task)
    if isinstance(input_grid, list):
         # Handle potential nested list like [[...]] for a single row
         if len(input_grid) == 1 and isinstance(input_grid[0], list):
              input_row = np.array(input_grid[0], dtype=int)
         else:
              input_row = np.array(input_grid, dtype=int)
    elif isinstance(input_grid, np.ndarray):
         input_row = input_grid.flatten() # Ensure 1D
    else:
        raise TypeError("Input grid must be a list or numpy array.")

    # Initialize output_grid as a copy of the input
    output_row = input_row.copy()

    # Find the non-white segment
    start_idx, end_idx = find_non_white_segment(input_row)

    # If no segment exists, return the original row
    if start_idx is None:
        # Reshape back to original if necessary (though examples are 1xN)
        # This might be needed if input was [[...]]
        if isinstance(input_grid, list) and len(input_grid) == 1 and isinstance(input_grid[0], list):
             return [output_row.tolist()]
        elif isinstance(input_grid, np.ndarray) and input_grid.ndim > 1:
             return output_row.reshape(input_grid.shape)
        return output_row.tolist() # Return as list to match example format

    # Extract the segment based on its start and end indices
    segment = input_row[start_idx : end_idx + 1]

    # Determine the dominant color within this segment
    dominant_color = get_dominant_color(segment)

    # Replace all pixels within the segment bounds in the output row with the dominant color
    output_row[start_idx : end_idx + 1] = dominant_color

    # Reshape back to original if necessary
    if isinstance(input_grid, list) and len(input_grid) == 1 and isinstance(input_grid[0], list):
         return [output_row.tolist()]
    elif isinstance(input_grid, np.ndarray) and input_grid.ndim > 1:
         return output_row.reshape(input_grid.shape)
         
    # Return the modified row as a list
    return output_row.tolist()
