import numpy as np
import copy

"""
Identify all maximal horizontal contiguous segments of gray (5) pixels in the input grid.
Determine the maximum length 'L' among these segments.
If no gray segments exist, return the input grid unchanged.
Filter the segments to find all segments with length 'L'.
Check if ANY of these longest segments satisfy a trigger condition:
  - The segment spans the full width of the grid.
  OR
  - The segment is 'bounded', meaning its left end is adjacent to a white (0) pixel or the grid edge, AND its right end is adjacent to a white (0) pixel or the grid edge.
If the trigger condition is met, change the color of ALL segments with length 'L' from gray (5) to maroon (9) in a copy of the input grid.
Otherwise, return the original input grid.
"""

def find_gray_segments(grid):
    """
    Finds all maximal horizontal contiguous segments of gray (5) pixels.

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of dictionaries, each representing a segment with keys:
              'row', 'start_col', 'end_col', 'length'.
              Returns an empty list if no gray segments are found.
    """
    segments = []
    height, width = grid.shape
    gray_color = 5

    for r in range(height):
        current_start = -1
        for c in range(width):
            is_gray = grid[r, c] == gray_color
            
            if is_gray and current_start == -1:
                # Start of a potential segment
                current_start = c
            elif not is_gray and current_start != -1:
                # End of a segment detected before end of row
                end_col = c - 1
                length = end_col - current_start + 1
                segments.append({'row': r, 'start_col': current_start, 'end_col': end_col, 'length': length})
                current_start = -1 # Reset for next potential segment

        # Check if a segment ends at the last column of the row
        if current_start != -1:
            end_col = width - 1
            length = end_col - current_start + 1
            segments.append({'row': r, 'start_col': current_start, 'end_col': end_col, 'length': length})

    return segments

def transform(input_grid):
    """
    Transforms the input grid based on the rules described above.
    Finds the longest horizontal gray segments. If any of these longest segments
    are full-width or bounded by white/edges, then all longest segments are
    recolored to maroon.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    output_grid = np.copy(grid) # Start with a copy
    height, width = grid.shape
    
    white_color = 0
    gray_color = 5
    maroon_color = 9

    # 1. Identify all horizontal gray segments
    segments = find_gray_segments(grid)

    # If no gray segments, return the original grid
    if not segments:
        return output_grid.tolist()

    # 2. Find the maximum length (L) among all segments
    max_len = 0
    if segments: # Ensure segments list is not empty
        max_len = max(segment['length'] for segment in segments)

    # If max_len is 0 (which implies no segments, but check just in case), return original
    if max_len == 0:
        return output_grid.tolist()

    # 3. Filter to get only the segments with the maximum length L
    longest_segments = [s for s in segments if s['length'] == max_len]

    # 4. Check the trigger condition for any of the longest segments
    should_recolor = False
    for segment in longest_segments:
        start_col = segment['start_col']
        end_col = segment['end_col']
        row_idx = segment['row']

        # Condition 1: Segment spans the full width
        is_full_width = (start_col == 0 and end_col == width - 1)

        # Condition 2: Segment is 'bounded'
        # Check left boundary: either grid edge (start_col == 0) or pixel to the left is white (0)
        left_bounded = (start_col == 0) or (grid[row_idx, start_col - 1] == white_color)
        # Check right boundary: either grid edge (end_col == width - 1) or pixel to the right is white (0)
        right_bounded = (end_col == width - 1) or (grid[row_idx, end_col + 1] == white_color)
        is_bounded = left_bounded and right_bounded

        # If any longest segment meets either condition, set the flag and stop checking
        if is_full_width or is_bounded:
            should_recolor = True
            break

    # 5. Apply transformation if the trigger condition was met
    if should_recolor:
        # Iterate through ALL segments with the maximum length L
        for segment in longest_segments:
            row_idx = segment['row']
            start_col = segment['start_col']
            end_col = segment['end_col']
            # Recolor the segment in the output grid from gray (5) to maroon (9)
            output_grid[row_idx, start_col : end_col + 1] = maroon_color
            
    # 6. Return the potentially modified grid as a list of lists
    return output_grid.tolist()