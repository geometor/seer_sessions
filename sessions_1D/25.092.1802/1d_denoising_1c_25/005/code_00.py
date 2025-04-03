"""
Identify all contiguous horizontal segments of non-background color (0) in the input row. 
Find the maximum length among these segments. Construct an output row of the same length, 
initially filled with the background color (0). Copy only those segments from the 
input row that have the maximum length into the output row at their original positions.
"""

import numpy as np
from typing import List, Dict, Any, Optional

def find_segments(row: List[int]) -> List[Dict[str, Any]]:
    """
    Identifies contiguous horizontal segments of non-background pixels in a row.

    Args:
        row: A list of integers representing a row of the grid.

    Returns:
        A list of dictionaries, where each dictionary represents a segment
        and contains 'color', 'start' (index), and 'length'. Returns an empty
        list if no non-background segments are found.
    """
    segments = []
    current_segment: Optional[Dict[str, Any]] = None
    background_color = 0

    for i, pixel in enumerate(row):
        if pixel != background_color:  # Non-background pixel
            if current_segment is None:
                # Start of a new segment
                current_segment = {'color': pixel, 'start': i, 'length': 1}
            elif pixel == current_segment['color']:
                # Continuation of the current segment of the same color
                current_segment['length'] += 1
            else:
                # End of the previous segment (different non-background color)
                segments.append(current_segment)
                # Start of a new segment with the new color
                current_segment = {'color': pixel, 'start': i, 'length': 1}
        else:  # Background pixel
            if current_segment is not None:
                # End of the current non-background segment
                segments.append(current_segment)
                current_segment = None
                
    # Add the last segment if the row ends with a non-background pixel
    if current_segment is not None:
        segments.append(current_segment)
        
    return segments

def transform(input_grid_list: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid by keeping only the longest non-background segment(s).
    """
    # Step 1: Validate input and extract the row.
    # Input should be a list containing exactly one list (the row).
    if not isinstance(input_grid_list, list) or len(input_grid_list) != 1 or not isinstance(input_grid_list[0], list):
        # Handle invalid input format, perhaps return empty or raise error
        # For ARC, returning an empty structure is usually preferred over raising errors.
        return [[]] 
        
    input_row = input_grid_list[0]
    
    # Handle empty row case
    if not input_row:
        return [[]]
        
    height = 1 # Task context implies single row
    width = len(input_row)
    background_color = 0 

    # Step 2: Initialize the output grid (as a numpy array for convenience).
    # Create a new row of the same length, filled with the background color.
    output_grid_np = np.full((height, width), background_color, dtype=int)

    # Step 3: Identify all contiguous segments of non-background colors.
    segments = find_segments(input_row)

    # Step 4: If no non-background segments are found, return the initialized background grid.
    if not segments:
        return output_grid_np.tolist() # Convert numpy array back to list of lists

    # Step 5: Find the maximum length among all identified segments.
    max_length = 0
    for segment in segments:
        if segment['length'] > max_length:
            max_length = segment['length']
            
    # This check might be redundant if step 4 already handled the 'no segments' case,
    # but it ensures safety if find_segments somehow returns segments with length 0.
    if max_length == 0:
         return output_grid_np.tolist()

    # Step 6: Iterate through segments and place the longest ones onto the output grid.
    # For each segment whose length equals the maximum length, copy its pixels.
    for segment in segments:
        if segment['length'] == max_length:
            start_col = segment['start']
            end_col = start_col + segment['length']
            color = segment['color']
            # Place the segment in the first (and only) row of the numpy array
            # Slicing handles placing the segment correctly.
            output_grid_np[0, start_col:end_col] = color

    # Step 7: Return the final output grid in the required List[List[int]] format.
    return output_grid_np.tolist()