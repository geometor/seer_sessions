import numpy as np
from typing import List, Tuple, Dict, Optional

"""
Isolate the single longest contiguous block of non-white pixels in a 1D input grid.
Replace all other pixels (original background and shorter non-white blocks) 
with the background color (White, 0).
"""

def find_non_white_segments(row: List[int]) -> List[Dict[str, int]]:
    """
    Identifies all contiguous segments of non-white pixels in a row.

    Args:
        row: A list of integers representing the pixel colors in the row.

    Returns:
        A list of dictionaries, where each dictionary represents a segment
        and contains 'start', 'end', 'length', and 'color'.
    """
    segments = []
    current_segment = None
    
    for i, pixel in enumerate(row):
        if pixel != 0:  # Non-white pixel
            if current_segment is None:
                # Start a new segment
                current_segment = {'start': i, 'color': pixel, 'length': 1}
            elif pixel == current_segment['color']:
                # Continue the current segment
                current_segment['length'] += 1
            else:
                # End the previous segment (different color)
                current_segment['end'] = i - 1
                segments.append(current_segment)
                # Start a new segment
                current_segment = {'start': i, 'color': pixel, 'length': 1}
        else:  # White pixel
            if current_segment is not None:
                # End the current segment
                current_segment['end'] = i - 1
                segments.append(current_segment)
                current_segment = None
                
    # Handle segment reaching the end of the row
    if current_segment is not None:
        current_segment['end'] = len(row) - 1
        segments.append(current_segment)
        
    return segments

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input 1D grid by keeping only the longest contiguous 
    non-white segment and making everything else white (0).

    Args:
        input_grid: A list containing a single list of integers (the 1D grid).

    Returns:
        A list containing a single list of integers representing the transformed grid.
    """
    # Ensure input is a 1D grid (represented as a list of one list)
    if len(input_grid) != 1:
        raise ValueError("Input grid must be 1D (have only one row).")
        
    input_row = input_grid[0]
    grid_length = len(input_row)
    
    # Initialize output grid with all white pixels
    output_row = [0] * grid_length

    # Find all non-white segments
    segments = find_non_white_segments(input_row)

    # Find the longest segment
    longest_segment: Optional[Dict[str, int]] = None
    max_length = 0
    
    if not segments:
        # No non-white segments found, return the all-white grid
        return [output_row]
        
    for segment in segments:
        if segment['length'] > max_length:
            max_length = segment['length']
            longest_segment = segment
        # Note: If multiple segments have the same max length, this picks the first one found.
        # The examples don't specify tie-breaking, so this behavior is assumed sufficient.

    # If a longest segment was found, copy it to the output grid
    if longest_segment:
        start = longest_segment['start']
        end = longest_segment['end']
        color = longest_segment['color']
        for i in range(start, end + 1):
            # Check bounds just in case, although segment finding should be correct
            if 0 <= i < grid_length:
                 output_row[i] = color

    # Return the output grid in the required format (list of lists)
    return [output_row]