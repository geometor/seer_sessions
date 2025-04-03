import numpy as np
from typing import List, Dict, Any, Optional

"""
This module transforms a 1D grid of pixels by finding a specific pattern
and swapping the positions of its components.

The pattern consists of:
1. A single 'marker' pixel (the first non-background pixel encountered).
2. A contiguous sequence of identical pixels ('color sequence') that 
   immediately follows the marker pixel and has a different color than it.

The transformation involves:
1. Moving the entire 'color sequence' to start at the original position 
   of the 'marker' pixel.
2. Moving the 'marker' pixel to the position immediately following the 
   end of the moved 'color sequence'.
Background pixels (color 0) remain unchanged.
"""

def find_pattern(grid: List[int]) -> Optional[Dict[str, Any]]:
    """
    Scans the grid to find the marker pixel and the adjacent color sequence.

    Args:
        grid: A 1D list representing the input grid pixels.

    Returns:
        A dictionary containing information about the found pattern 
        (marker index, marker color, sequence start index, sequence end index, 
        sequence color), or None if the pattern is not found or invalid.
    """
    marker_index = -1
    marker_color = -1
    seq_start_index = -1
    seq_color = -1
    seq_end_index = -1
    grid_len = len(grid)

    # Find the first non-background pixel (marker)
    for i, pixel in enumerate(grid):
        if pixel != 0:
            marker_index = i
            marker_color = pixel
            break

    # Check if a marker was found and if there's space for a sequence after it
    if marker_index == -1 or marker_index >= grid_len - 1:
        return None # No marker found or no space for sequence

    # Find the start of the sequence (must be non-background and different color)
    seq_start_index = marker_index + 1
    if grid[seq_start_index] == 0 or grid[seq_start_index] == marker_color:
        return None # Invalid sequence start
    seq_color = grid[seq_start_index]
    seq_end_index = seq_start_index # Sequence is at least one pixel long

    # Find the end of the contiguous sequence of the same color
    for i in range(seq_start_index + 1, grid_len):
        if grid[i] == seq_color:
            seq_end_index = i
        else:
            break # Sequence ends

    return {
        "marker_index": marker_index,
        "marker_color": marker_color,
        "seq_start_index": seq_start_index,
        "seq_end_index": seq_end_index,
        "seq_color": seq_color
    }

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid by swapping the marker pixel and the adjacent color sequence.

    Args:
        input_grid: A numpy array representing the input grid. 
                      Expected to be 1D or 2D with a single row.

    Returns:
        A numpy array representing the transformed grid, maintaining the original shape.
    """
    # Ensure input is a NumPy array and handle potential multi-row inputs
    # For this task, we expect 1xN or N shape. Flatten to 1D list for processing.
    if not isinstance(input_grid, np.ndarray):
        input_grid = np.array(input_grid)
        
    original_shape = input_grid.shape
    # Flatten the grid to a 1D list for easier processing
    input_list = input_grid.flatten().tolist()
    
    # Initialize output_list as a copy of the input_list
    output_list = list(input_list)

    # Locate the marker and the sequence
    pattern_info = find_pattern(input_list)

    # If the specific pattern isn't found, return the original grid unchanged
    if pattern_info is None:
        # print("Warning: Required pattern not found. Returning original grid.")
        return input_grid # Return original numpy array

    # Extract pattern details
    marker_index = pattern_info["marker_index"]
    marker_color = pattern_info["marker_color"]
    seq_start_index = pattern_info["seq_start_index"]
    seq_end_index = pattern_info["seq_end_index"]
    seq_color = pattern_info["seq_color"]

    # Calculate the length of the color sequence
    seq_length = seq_end_index - seq_start_index + 1

    # Perform the swap in the output list
    # 1. Place the color sequence starting at the original marker position
    for i in range(seq_length):
        # Check bounds just in case, although pattern finding should ensure validity
        if marker_index + i < len(output_list):
            output_list[marker_index + i] = seq_color

    # 2. Place the marker pixel immediately after the newly placed sequence
    new_marker_position = marker_index + seq_length
    if new_marker_position < len(output_list):
         output_list[new_marker_position] = marker_color
    # Note: This logic assumes the swap doesn't overwrite essential parts before they are used.
    # Since we work on a copy `output_list` based on `input_list`, this is safe.

    # Convert the result list back to a numpy array with the original shape
    output_grid = np.array(output_list).reshape(original_shape)

    return output_grid