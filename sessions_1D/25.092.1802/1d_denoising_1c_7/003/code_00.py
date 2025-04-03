"""
Identify all contiguous segments of non-white pixels (non-zero values) in the input row array. 
Find the segment with the maximum length. 
Create an output NumPy array of the same shape as the input, filled with white pixels (zeros).
Copy the pixels corresponding to the single longest segment from the input row array 
to the same positions in the output array.
"""

import numpy as np
from typing import List, Dict, Optional

def find_segments_np(row: np.ndarray) -> List[Dict]:
    """
    Finds contiguous non-zero segments in a 1D NumPy array.

    Args:
        row: A 1D NumPy array representing pixel colors.

    Returns:
        A list of dictionaries, where each dictionary represents a segment
        and contains 'color' (value of the first pixel in segment), 
        'start_index', and 'length'. Returns an empty list if no 
        non-zero segments are found.
    """
    segments = []
    # Check if the input is a 1D array
    if row.ndim != 1:
        # This case shouldn't happen with valid ARC input for this task, 
        # but good practice to check.
        return segments 
        
    # Pad the boolean array (non-zero elements) to detect changes at edges
    padded_non_zero = np.concatenate(([0], (row != 0).astype(int), [0]))
    
    # Find where segments start (0 to 1 transition) and end (1 to 0 transition)
    diff = np.diff(padded_non_zero)
    starts = np.where(diff == 1)[0]
    ends = np.where(diff == -1)[0]
    
    # Create segment dictionaries
    for i in range(len(starts)):
        start_index = starts[i]
        # End index from diff is exclusive, so length is end - start
        length = ends[i] - start_index 
        # Ensure the segment has positive length and start index is valid
        if length > 0 and start_index < len(row):
             # Get the color from the first pixel of the segment in the original row
             color = row[start_index]
             # Ensure the detected segment isn't background accidentally captured
             if color != 0:
                 segments.append({'color': int(color), 'start_index': int(start_index), 'length': int(length)})

    return segments

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid by keeping only the longest contiguous segment 
    of non-zero pixels in the row.

    Args:
        input_grid: A 2D NumPy array, expected shape (1, N), representing the input grid.

    Returns:
        A 2D NumPy array of the same shape as the input, containing only the 
        longest segment from the input row, with other pixels set to 0.
    """
    # Validate input shape - should be (1, N)
    if input_grid.ndim != 2 or input_grid.shape[0] != 1:
        # Handle unexpected input shape if necessary, maybe return input or raise error
        # For now, assume valid input based on examples.
        # If the input is truly empty or malformed according to task rules,
        # returning an empty array of appropriate shape might be needed.
        # Let's default to returning a zero array of the input shape.
        return np.zeros_like(input_grid)

    # Extract the 1D row from the input grid
    input_row = input_grid[0]
    
    # Initialize the output grid with zeros (white) - same shape as input
    output_grid = np.zeros_like(input_grid)

    # Find all non-zero segments in the input row
    segments = find_segments_np(input_row)

    # If no non-zero segments are found, return the all-zero grid
    if not segments:
        return output_grid

    # Find the longest segment among the identified ones
    # If there's a tie in length, max() typically returns the first one encountered.
    longest_segment: Optional[Dict] = None
    max_length = 0
    for segment in segments:
        if segment['length'] > max_length:
            max_length = segment['length']
            longest_segment = segment
            
    # If a longest segment was found (it should be if segments list wasn't empty)
    if longest_segment:
        # Get the details of the longest segment
        start = longest_segment['start_index']
        length = longest_segment['length']
        
        # Copy the pixels corresponding to the longest segment 
        # from the original input row to the output grid's row
        # Ensure slicing doesn't go out of bounds (shouldn't with correct segment finding)
        end = start + length
        output_grid[0, start:end] = input_row[start:end]

    # Return the final output grid
    return output_grid