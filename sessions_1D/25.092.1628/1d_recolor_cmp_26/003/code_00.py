"""
Change the color of specific horizontal blue segments (color 1) to yellow (color 4) based on their length relative to the longest horizontal blue segment(s) in the grid. Specifically, change segments whose length is equal to the maximum length found or one less than the maximum length.
"""

import numpy as np
from typing import List, Tuple

# Define type hints for clarity
Grid = List[List[int]]
Segment = Tuple[int, int, int, int] # (row, start_col, end_col, length)

def find_horizontal_blue_segments(grid: Grid) -> List[Segment]:
    """
    Identifies all contiguous horizontal segments of blue (1) pixels in the grid.

    Args:
        grid: The input grid (list of lists).

    Returns:
        A list of tuples, where each tuple represents a segment:
        (row_index, start_column, end_column, length).
    """
    segments = []
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0
    blue_color = 1 # The color we are looking for (blue)

    # Iterate through each row
    for r in range(height):
        c = 0
        # Iterate through columns within the row
        while c < width:
            # Check if the current pixel is the target color (blue)
            if grid[r][c] == blue_color:
                start_col = c
                # Find the end of the contiguous segment of blue pixels
                while c < width and grid[r][c] == blue_color:
                    c += 1
                end_col = c - 1
                # Calculate the length of the segment
                length = end_col - start_col + 1
                # Store the segment details
                segments.append((r, start_col, end_col, length))
            else:
                # Move to the next column if not blue
                c += 1
    return segments

def transform(input_grid: Grid) -> Grid:
    """
    Transforms the input grid according to the specified rule.
    """
    # Convert input grid to a numpy array for easier manipulation and copying
    np_grid = np.array(input_grid, dtype=int)
    # Create a copy to modify, leaving the original input untouched
    output_grid = np_grid.copy()
    
    target_color = 1      # Blue
    change_to_color = 4   # Yellow

    # Find all horizontal segments of the target color (blue=1)
    segments = find_horizontal_blue_segments(output_grid.tolist()) # Use helper function

    # If no blue segments are found, no changes are needed, return the copy
    if not segments:
        return output_grid.tolist()

    # Determine the maximum length among all found segments
    max_len = 0
    for _, _, _, length in segments:
        if length > max_len:
            max_len = length
            
    # Define the lengths that qualify for a color change
    target_lengths = {max_len, max_len - 1}

    # Iterate through the found segments again
    for r, start_c, end_c, length in segments:
        # Check if the segment's length matches the target lengths
        if length in target_lengths:
            # Modify the output grid: change pixels in this segment to yellow
            for c in range(start_c, end_c + 1):
                 # Ensure the pixel is still the original target color before changing
                 # (Handles potential overlaps, though not expected in this specific rule)
                 if output_grid[r, c] == target_color:
                    output_grid[r, c] = change_to_color

    # Convert the final numpy array back to a list of lists for the standard ARC format
    return output_grid.tolist()