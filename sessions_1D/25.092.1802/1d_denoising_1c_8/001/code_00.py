import numpy as np
from typing import List, Tuple

"""
Identify all contiguous horizontal segments of non-white pixels in the input row. 
Find the segment with the maximum length. 
Create an output row of the same size, initialized to the background color (white, 0). 
Place only the single longest segment found into the output row at its original position. 
All other pixels remain white.
"""

def find_segments(input_row: np.ndarray) -> List[Tuple[int, int, int, int]]:
    """
    Finds contiguous segments of non-white pixels in a 1D numpy array.

    Args:
        input_row: A 1D numpy array representing a row of pixels.

    Returns:
        A list of tuples, where each tuple represents a segment:
        (start_index, end_index, length, color)
    """
    segments = []
    in_segment = False
    start_index = -1
    segment_color = -1
    
    # Add a padding of 0 at the end to handle segments ending at the last pixel
    padded_row = np.append(input_row, 0) 
    
    for i, pixel in enumerate(padded_row):
        if not in_segment and pixel != 0:
            # Start of a new segment
            in_segment = True
            start_index = i
            segment_color = pixel
        elif in_segment and (pixel == 0 or pixel != segment_color):
            # End of the current segment
            end_index = i - 1
            length = end_index - start_index + 1
            segments.append((start_index, end_index, length, segment_color))
            in_segment = False
            start_index = -1
            segment_color = -1
            # Check if the current pixel starts a new segment immediately
            if pixel != 0:
                in_segment = True
                start_index = i
                segment_color = pixel

    return segments

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid by keeping only the longest contiguous segment 
    of non-white pixels.

    Args:
        input_grid: A 1D numpy array representing the input row.

    Returns:
        A 1D numpy array representing the transformed output row.
    """
    
    # Ensure input is treated as a 1D array (even if passed as 1xN)
    input_row = input_grid.flatten()
    
    # Initialize output_grid with the background color (0)
    output_grid = np.zeros_like(input_row)
    
    # Find all non-white segments in the input row
    segments = find_segments(input_row)
    
    # If no segments are found, return the blank grid
    if not segments:
        return output_grid.reshape(input_grid.shape) # Reshape back to original input shape
        
    # Find the segment with the maximum length
    longest_segment = max(segments, key=lambda x: x[2])
    
    # Extract details of the longest segment
    start_index, end_index, _, _ = longest_segment
    
    # Copy the longest segment from the input to the output grid
    output_grid[start_index : end_index + 1] = input_row[start_index : end_index + 1]
    
    # Reshape the output to match the original input grid's shape (e.g., 1xN)
    return output_grid.reshape(input_grid.shape)
