import numpy as np
from collections import Counter

"""
Identifies the most frequent non-white color in the central segment of a single-row input grid 
and replaces all other non-white colors in that row with this dominant color. 
White (0) pixels at the beginning and end of the row (padding) remain unchanged.
"""

def find_non_white_segment(row):
    """Finds the start and end indices of the non-white segment."""
    start_index = -1
    end_index = -1
    for i, pixel in enumerate(row):
        if pixel != 0:
            if start_index == -1:
                start_index = i
            end_index = i
    if start_index == -1: # Row is all white
        return None, None
    return start_index, end_index + 1 # Slice is exclusive at the end

def find_dominant_color(segment):
    """Finds the most frequent color in a given segment."""
    if not segment:
        return None # No segment to analyze

    # Count occurrences of each color
    color_counts = Counter(segment)

    # Find the most frequent color
    # If there are ties, most_common(1) returns one of the most frequent
    if not color_counts:
        return None # Segment was empty or contained only white (already filtered?)
        
    # Ensure we are not selecting white if it somehow sneaks in
    # Although the segment definition should prevent this.
    # Adding safety check:
    if 0 in color_counts:
        del color_counts[0]
        
    if not color_counts: # Only contained white
        return None
        
    dominant_color, _ = color_counts.most_common(1)[0]
    return dominant_color

def transform(input_grid):
    """
    Applies the color normalization transformation to the input grid.
    
    Args:
        input_grid (list of lists): A 1xN grid represented as a list containing a single list.

    Returns:
        list of lists: The transformed 1xN grid.
    """
    # The input is expected to be a list containing one list (the row)
    if not input_grid or not input_grid[0]:
        return [] # Handle empty input

    input_row = input_grid[0]
    height = 1
    width = len(input_row)

    # Initialize the output grid as a copy initially
    # Convert to numpy array for easier manipulation if needed, but list comprehension works too
    output_row = list(input_row) # Create a mutable copy

    # 1. Find the segment of non-white pixels
    start_index, end_index = find_non_white_segment(input_row)

    # If no non-white segment exists (all white), return the original row
    if start_index is None:
        return [output_row] 

    # 2. Extract the non-white segment for analysis
    non_white_segment = input_row[start_index:end_index]

    # 3. Identify the dominant color within this segment
    dominant_color = find_dominant_color(non_white_segment)
    
    # If no dominant color found (e.g., segment only had white pixels, though find_non_white_segment should prevent this)
    # Or if there's only one color type, no transformation needed within the segment.
    # The loop below handles this correctly. If dominant_color is None, nothing will be changed.

    # 4. Create the output row by applying the transformation rule
    if dominant_color is not None: # Proceed only if a dominant color was found
        for i in range(width):
            # Check if the current pixel is within the non-white segment identified earlier
            # (This also handles the leading/trailing white padding implicitly)
            if i >= start_index and i < end_index:
                # If the pixel is not the dominant color and not white (0)
                if input_row[i] != dominant_color and input_row[i] != 0:
                    # Replace it with the dominant color
                    output_row[i] = dominant_color
            # Pixels outside the segment (padding) or pixels that are already the dominant color remain unchanged
            # White pixels within the segment (if any, though unlikely by definition) also remain unchanged

    # Return the transformed row within a list to match the grid format
    return [output_row]