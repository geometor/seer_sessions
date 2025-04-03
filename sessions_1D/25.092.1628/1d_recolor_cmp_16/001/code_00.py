"""
Identifies all contiguous horizontal segments of blue (1) pixels.
Determines the maximum length among these segments.
Changes the color of all blue segments that have this maximum length to green (3).
All other pixels remain unchanged.
"""

import numpy as np

def find_horizontal_segments(grid, target_color):
    """
    Finds all contiguous horizontal segments of a specific color in the grid.

    Args:
        grid (np.array): The input grid.
        target_color (int): The color of the segments to find.

    Returns:
        list: A list of tuples, where each tuple represents a segment:
              (row_index, start_col_index, end_col_index, length).
    """
    segments = []
    height, width = grid.shape
    for r in range(height):
        start_col = -1
        for c in range(width):
            # Check if the current pixel is the target color
            if grid[r, c] == target_color:
                # If we are not already tracking a segment, start one
                if start_col == -1:
                    start_col = c
            # If the current pixel is NOT the target color
            else:
                # If we were tracking a segment, it just ended
                if start_col != -1:
                    end_col = c - 1
                    length = end_col - start_col + 1
                    segments.append((r, start_col, end_col, length))
                    start_col = -1 # Reset start_col
        # Check if a segment was ongoing at the end of the row
        if start_col != -1:
            end_col = width - 1
            length = end_col - start_col + 1
            segments.append((r, start_col, end_col, length))
            
    return segments

def transform(input_grid):
    """
    Transforms the input grid by changing the color of the longest horizontal
    segment(s) of blue pixels to green.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the output grid.
    """
    # Define colors
    blue = 1
    green = 3

    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)

    # Find all horizontal segments of blue pixels
    blue_segments = find_horizontal_segments(output_grid, blue)

    # If no blue segments are found, return the original grid
    if not blue_segments:
        return output_grid

    # Determine the maximum length among the blue segments
    max_length = 0
    for segment in blue_segments:
        length = segment[3]
        if length > max_length:
            max_length = length

    # Iterate through the identified blue segments again
    for segment in blue_segments:
        r, start_c, end_c, length = segment
        # If a segment's length matches the maximum length
        if length == max_length:
            # Change the color of pixels in this segment to green
            for c in range(start_c, end_c + 1):
                output_grid[r, c] = green

    return output_grid