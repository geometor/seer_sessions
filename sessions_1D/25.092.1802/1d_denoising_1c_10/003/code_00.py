import numpy as np
from typing import List, Tuple, Dict, Any, Optional

"""
Identify all contiguous horizontal segments of non-background pixels (value > 0) in the input row.
Determine the length of each segment.
Find the segment with the greatest length. 
Create a new output row of the same length as the input, filled entirely with the background color (white, 0).
Copy the pixels (color and position) from the single longest segment identified from the input row to the corresponding positions in the new output row. All other pixels in the output row remain the background color.
Return the new output row as a single-row grid.
"""

def find_longest_segment_details(row: List[int]) -> Optional[Dict[str, Any]]:
    """
    Finds the longest contiguous segment of non-zero values in a list.

    Args:
        row: A list of integers representing a row of pixels.

    Returns:
        A dictionary containing 'start', 'end', 'length', and 'color' 
        of the longest segment, or None if no non-zero segment is found.
        If multiple segments share the maximum length, the first one encountered is returned.
    """
    max_len = 0
    longest_segment_info = None

    current_start = -1
    current_len = 0
    current_color = 0

    for i, pixel in enumerate(row):
        # Start or continuation of a segment
        if pixel != 0:
            if current_start == -1: # Starting a new segment
                current_start = i
                current_len = 1
                current_color = pixel
            elif pixel == current_color: # Continuing the current segment
                 current_len += 1
            else: # Color changed mid-segment (treat as end of old, start of new)
                 # First, process the just-ended segment
                 if current_start != -1:
                    if current_len > max_len:
                         max_len = current_len
                         longest_segment_info = {'start': current_start, 'end': i - 1, 'length': current_len, 'color': current_color}
                 # Then, start the new segment
                 current_start = i
                 current_len = 1
                 current_color = pixel
        
        # End of a segment (current pixel is 0)
        elif pixel == 0 and current_start != -1:
             if current_len > max_len:
                 max_len = current_len
                 longest_segment_info = {'start': current_start, 'end': i - 1, 'length': current_len, 'color': current_color}
             # Reset current segment tracking
             current_start = -1
             current_len = 0
             current_color = 0
                
    # Check if a segment ended exactly at the last element
    if current_start != -1:
        if current_len > max_len:
             max_len = current_len
             longest_segment_info = {'start': current_start, 'end': len(row) - 1, 'length': current_len, 'color': current_color}

    return longest_segment_info


def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid by keeping only the longest contiguous segment
    of non-background pixels in the single row.

    Args:
        input_grid: A list containing a single list of integers (a 1xN grid), 
                    potentially passed as a NumPy array.

    Returns:
        A new list containing a single list of integers, representing the transformed grid.
    """
    # Convert input to list of lists if it's a numpy array for consistent processing
    if isinstance(input_grid, np.ndarray):
        input_grid = input_grid.tolist()
        
    # Ensure input is not empty and has at least one row
    if not input_grid or not input_grid[0]:
        return [] # Return empty list for empty input

    input_row = input_grid[0]
    width = len(input_row)
    background_color = 0

    # Initialize output row with background color
    output_row = [background_color] * width

    # Find the details of the longest segment in the input row
    longest_segment = find_longest_segment_details(input_row)

    # If a longest segment was found
    if longest_segment:
        start = longest_segment['start']
        end = longest_segment['end']
        
        # Copy the pixels of the longest segment from input to output
        # We can just copy the original pixel values as they define the segment
        for i in range(start, end + 1):
             if i < width: # Ensure index is within bounds
                output_row[i] = input_row[i]

    # Return the transformed row within a list to match grid format
    output_grid = [output_row]
    return output_grid