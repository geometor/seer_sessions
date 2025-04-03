import numpy as np
from typing import List, Dict, Any

def find_contiguous_segments(row: List[int], target_color: int) -> List[Dict[str, Any]]:
    """
    Finds all contiguous segments of a target color in a 1D list (row).

    Args:
        row: A list of integers representing a row of the grid.
        target_color: The integer color value to find segments of.

    Returns:
        A list of dictionaries, where each dictionary represents a segment
        and contains 'start' (index), 'end' (index), 'length', and 'color'.
        Returns an empty list if no segments are found.
    """
    segments = []
    start_index = -1
    for i, pixel in enumerate(row):
        if pixel == target_color and start_index == -1:
            # Start of a new segment
            start_index = i
        elif pixel != target_color and start_index != -1:
            # End of the current segment (pixel at i is not part of it)
            segments.append({'start': start_index, 'end': i - 1, 'length': i - start_index, 'color': target_color})
            start_index = -1
            
    # Check if the row ends with an active segment
    if start_index != -1:
        segments.append({'start': start_index, 'end': len(row) - 1, 'length': len(row) - start_index, 'color': target_color})
        
    return segments

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid by identifying the primary non-white color, finding
    all its contiguous horizontal segments, selecting the longest segment, and
    creating an output grid containing only this longest segment against a
    white background.

    Args:
        input_grid: A list of lists representing the input grid. Assumed to be 1xN.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Convert to numpy array for easier handling
    input_array = np.array(input_grid, dtype=int)
    
    # Ensure input is treated as 1xN as per examples
    if input_array.shape[0] != 1:
        # This case is not explicitly handled by examples, but we proceed assuming the first row is relevant
        # or the task implies 1D structure flattened into a single row list.
        # If input_grid was [[1,2,3]], input_array would be [[1,2,3]] with shape (1,3)
        # If input_grid was [[1],[2],[3]], input_array would be [[1],[2],[3]] with shape (3,1) - this needs clarification.
        # Assuming the format is always [[...]] representing a single row.
        if input_array.ndim == 1: # If input somehow became 1D numpy array e.g. np.array([0,0,7...])
             input_array = input_array.reshape(1, -1) # Reshape to 1xN
        elif input_array.shape[0] > 1 and input_array.shape[1] == 1: # Column vector case
             input_array = input_array.T # Transpose to row vector
        # For other >1 height cases, we'll just use the first row, though this might be incorrect for general cases.
        pass # Keep working with input_array, potentially focusing on the first row below.


    height, width = input_array.shape
    
    # Initialize output grid with background color (white, 0)
    output_array = np.zeros_like(input_array)

    # Get the single row data (assuming 1xN structure)
    # If height > 1, this takes the first row.
    row_data = input_array[0].tolist() 

    # 1. Identify the primary non-white color
    #    Iterate through the row to find the first non-zero pixel.
    non_white_color = 0
    for pixel in row_data:
        if pixel != 0:
            non_white_color = pixel
            break

    # If the grid is all white or no non-white color is found, return the zero grid
    if non_white_color == 0:
        return output_array.tolist()

    # 2. Find all contiguous segments of the non-white color in the row
    segments = find_contiguous_segments(row_data, non_white_color)

    # If no segments were found (e.g., non_white_color identified but not in a segment?), return zero grid
    if not segments:
        return output_array.tolist()

    # 3. Find the segment with the maximum length
    #    If there's a tie, max() returns the first one encountered.
    longest_segment = max(segments, key=lambda s: s['length'])

    # 4. Copy the longest segment to the output grid
    #    Place the segment's color in the corresponding positions in the output array's first row.
    start_col = longest_segment['start']
    end_col = longest_segment['end']
    output_array[0, start_col : end_col + 1] = longest_segment['color']

    # 5. Return the result as a list of lists
    return output_array.tolist()