"""
Identify the longest contiguous horizontal segment(s) of the single non-white color present in the input grid's row.
Output a grid of the same dimensions containing only these longest segment(s) against a white background (color 0).
If multiple segments share the maximum length, include all of them.
If the input is all white or contains no non-white segments, the output is an all-white grid of the same dimensions.
Assumes the input grid has exactly one row.
"""

import numpy as np
from typing import List, Tuple, Any # Use Any for input_grid to be flexible

def find_segments(row: np.ndarray, target_color: int) -> List[Tuple[int, int, int]]:
    """
    Finds all contiguous segments of a specific color in a 1D numpy array (row).

    Args:
        row: The input 1D numpy array representing the row.
        target_color: The color of the segments to find (must be non-zero).

    Returns:
        A list of tuples, where each tuple represents a segment:
        (start_index, end_index, length). Returns an empty list if
        target_color is 0 or not found.
    """
    if target_color == 0:
        return [] # Background color cannot form segments of interest

    segments = []
    start_index = -1
    n = len(row)

    for i, pixel in enumerate(row):
        if pixel == target_color and start_index == -1:
            # Start of a new segment
            start_index = i
        elif pixel != target_color and start_index != -1:
            # End of the current segment (index i-1)
            end_index = i - 1
            length = end_index - start_index + 1
            segments.append((start_index, end_index, length))
            start_index = -1 # Reset for the next potential segment

    # Check if a segment was ongoing at the very end of the row
    if start_index != -1:
        end_index = n - 1
        length = end_index - start_index + 1
        segments.append((start_index, end_index, length))

    return segments

def transform(input_grid: Any) -> List[List[int]]:
    """
    Transforms the input grid (assumed 1xN) by isolating the longest 
    contiguous horizontal segment(s) of the non-white color in its row.

    Args:
        input_grid: A list of lists or numpy array representing the input grid (e.g., [[...]]).

    Returns:
        A list of lists representing the output grid with the transformation applied.
    """
    # Convert input to numpy array for easier processing and access dimensions
    input_array = np.array(input_grid, dtype=int)
    
    # Ensure input is 2D, even if passed as 1D list (unlikely in ARC but good practice)
    if input_array.ndim == 1:
        input_array = np.expand_dims(input_array, axis=0)
        
    height, width = input_array.shape

    # Handle cases where input dimensions are unexpected (e.g., height != 1)
    # Based on examples, we assume height is always 1. If not, the logic might need adjustment.
    # For now, proceed assuming height == 1.
    if height != 1:
         # Decide how to handle multi-row grids if they occur.
         # For this problem, based on examples, return an empty or zero grid might be appropriate
         # if the assumption of H=1 is violated. Or process each row independently?
         # Sticking to the observed pattern: operate only on the first row if H > 1,
         # or simply return an empty grid if that's safer.
         # Let's return an all-white grid of original dimensions if H != 1.
         # print(f"Warning: Expected input height 1, got {height}. Returning zero grid.")
         return np.zeros_like(input_array).tolist()


    # Extract the first (and only) row
    input_row = input_array[0]

    # Initialize output grid with background color (0)
    output_array = np.zeros_like(input_array, dtype=int)
    output_row = output_array[0] # Get a view of the output row to modify

    # 1. Identify the unique non-white color (C) in the row
    unique_colors = np.unique(input_row)
    non_white_color = 0
    for color in unique_colors:
        if color != 0:
            non_white_color = color
            break # Assuming only one non-white color as per examples

    # Handle case where the row is all white (non_white_color remains 0)
    if non_white_color == 0:
        return output_array.tolist() # Return the all-zero grid

    # 2. Find all contiguous segments of color C in the row
    segments = find_segments(input_row, non_white_color)

    # Handle case where no segments of the target color are found
    if not segments:
        return output_array.tolist() # Return the all-zero grid

    # 3. Find the maximum length among the segments
    max_length = 0
    for _, _, length in segments:
        if length > max_length:
            max_length = length

    # If max_length is still 0 (shouldn't happen if segments were found), return zero grid
    if max_length == 0:
         return output_array.tolist()

    # 4. Identify all segments with the maximum length
    longest_segments = []
    for start, end, length in segments:
        if length == max_length:
            longest_segments.append((start, end))

    # 5. Populate the output row with the pixels from the longest segments
    for start, end in longest_segments:
        # Fill the corresponding indices in the output row with the non_white_color
        output_row[start:end + 1] = non_white_color

    # 6. Return the result as a list of lists
    return output_array.tolist()