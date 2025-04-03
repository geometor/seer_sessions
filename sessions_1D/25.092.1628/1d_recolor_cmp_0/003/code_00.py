"""
Transforms the input grid by identifying all contiguous horizontal segments of red (2) pixels in the single row. It then determines the maximum length among these red segments. Finally, it changes the color of all red segments that match this maximum length to blue (1). Other pixels (white pixels and red pixels in segments not matching the maximum length) remain unchanged.
"""

import numpy as np

def find_contiguous_segments(grid_row, target_color):
    """
    Finds contiguous segments of a target color in a 1D numpy array (grid row).

    Args:
        grid_row (np.array): A 1D numpy array representing a row of the grid.
        target_color (int): The color value to search for segments of.

    Returns:
        list: A list of dictionaries, where each dictionary represents a segment
              and contains {'start': start_index, 'end': end_index, 'length': length}.
              Returns an empty list if no segments are found.
    """
    segments = []
    start_index = None
    for i, pixel in enumerate(grid_row):
        if pixel == target_color:
            if start_index is None:
                start_index = i  # Start of a potential segment
        elif start_index is not None:
            # End of the segment found (current pixel is different)
            end_index = i - 1
            length = end_index - start_index + 1
            segments.append({'start': start_index, 'end': end_index, 'length': length})
            start_index = None # Reset for next segment

    # Check if a segment extends to the end of the row
    if start_index is not None:
        end_index = len(grid_row) - 1
        length = end_index - start_index + 1
        segments.append({'start': start_index, 'end': end_index, 'length': length})

    return segments

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid (expected 1xN).

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    # Ensure input is a numpy array
    if not isinstance(input_grid, np.ndarray):
        input_grid = np.array(input_grid)

    # Handle empty input
    if input_grid.size == 0:
        return input_grid.copy()
        
    # Initialize output_grid as a copy of the input_grid
    output_grid = input_grid.copy()

    # Define the target color (red) and the replacement color (blue)
    target_color = 2
    replacement_color = 1

    # Access the single row (assuming input is always 1xN)
    # Check if the grid has at least one row before accessing it
    if input_grid.shape[0] == 0:
        return output_grid # Return copy if no rows
        
    input_row = input_grid[0]
    output_row = output_grid[0] # We will modify this row directly

    # Find all contiguous segments of the target color (red)
    red_segments = find_contiguous_segments(input_row, target_color)

    # If no red segments are found, return the original grid copy
    if not red_segments:
        return output_grid

    # Determine the maximum length among all identified red segments
    max_length = 0
    for segment in red_segments:
        if segment['length'] > max_length:
            max_length = segment['length']

    # Iterate through the found segments again
    for segment in red_segments:
        # Check if the segment has the maximum length
        if segment['length'] == max_length:
            # Modify the corresponding pixels in the output grid row
            start = segment['start']
            end = segment['end']
            # Use slicing to update the output row
            output_row[start : end + 1] = replacement_color

    # Return the modified grid
    # The output_grid was modified in place via output_row
    return output_grid