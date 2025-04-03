import numpy as np
from typing import List, Tuple, Dict, Optional

"""
Identify the longest contiguous horizontal segment of maroon (9) pixels in the input grid. 
Change the color of the pixels belonging to this longest segment to red (2) in the output grid. 
All other pixels retain their original color.
"""

def find_horizontal_segments(grid: np.ndarray, color: int) -> List[Dict]:
    """
    Finds all contiguous horizontal segments of a given color in the grid.

    Args:
        grid: The input grid as a numpy array.
        color: The integer color value to search for.

    Returns:
        A list of dictionaries, where each dictionary represents a segment
        and contains 'row', 'start_col', 'end_col', and 'length'.
    """
    segments = []
    height, width = grid.shape
    for r in range(height):
        current_segment_start = -1
        for c in range(width):
            # Start of a potential segment
            if grid[r, c] == color and current_segment_start == -1:
                current_segment_start = c
            # End of a segment (different color or end of row)
            if (grid[r, c] != color or c == width - 1) and current_segment_start != -1:
                # Adjust end column if the segment ended before the last column
                end_col = c - 1 if grid[r, c] != color else c
                length = end_col - current_segment_start + 1
                segments.append({
                    'row': r,
                    'start_col': current_segment_start,
                    'end_col': end_col,
                    'length': length
                })
                current_segment_start = -1 # Reset for the next potential segment
    return segments

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid by finding the longest horizontal segment of 
    maroon (9) pixels and changing its color to red (2).

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Convert input to numpy array for easier processing
    grid_np = np.array(input_grid, dtype=int)
    
    # Initialize output_grid as a copy of the input
    output_grid_np = grid_np.copy()

    # Define target and replacement colors
    target_color = 9  # maroon
    replacement_color = 2 # red

    # 1. Find all horizontal segments of the target color (maroon)
    maroon_segments = find_horizontal_segments(grid_np, target_color)

    # 2. Check if any segments were found
    if not maroon_segments:
        return input_grid # Return original grid if no maroon segments exist

    # 3. Find the segment with the maximum length
    longest_segment = None
    max_length = 0
    for segment in maroon_segments:
        if segment['length'] > max_length:
            max_length = segment['length']
            longest_segment = segment
        # Note: The current logic assumes a unique longest segment based on examples.
        # If multiple segments share the max length, this picks the first one encountered.

    # 4. If a longest segment was found, recolor its pixels in the output grid
    if longest_segment:
        row = longest_segment['row']
        start_col = longest_segment['start_col']
        end_col = longest_segment['end_col']
        # Change the color of these specific pixels in the output grid
        output_grid_np[row, start_col:end_col + 1] = replacement_color

    # Convert the numpy array back to a list of lists for the final output
    return output_grid_np.tolist()