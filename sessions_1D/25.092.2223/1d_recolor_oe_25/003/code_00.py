"""
Recolors contiguous horizontal segments of gray (5) pixels in a 1xN grid.
The transformation depends on the total number of gray segments and the length parity of consecutive segments.

1. Identify all contiguous horizontal segments of gray (5).
2. Determine the starting color based on the total number of segments:
   - If the total count is odd, the first segment becomes azure (8).
   - If the total count is even, the first segment becomes maroon (9).
3. Assign colors to subsequent segments based on the previous segment's color and the length parity of both the current and previous segments:
   - If both the current segment and the immediately preceding segment have lengths that are even, the current segment retains the same color as the previous one.
   - Otherwise, the current segment's color alternates from the previous segment's color (8 becomes 9, 9 becomes 8).
4. White (0) pixels remain unchanged.
"""

import numpy as np

def find_gray_segments_1d(grid_row):
    """
    Finds all contiguous horizontal segments of gray (5) pixels in a 1D numpy array (a single row).

    Args:
        grid_row: A 1D numpy array representing a row of the grid.

    Returns:
        A list of dictionaries, where each dictionary represents a segment
        and contains keys 'start_col', 'end_col', and 'length'.
        The list is ordered by the scanning order (left-to-right).
    """
    segments = []
    width = len(grid_row)
    c = 0
    while c < width:
        # Look for the start of a gray segment
        if grid_row[c] == 5:
            start_col = c
            end_col = c
            # Extend the segment to the right
            nc = c + 1
            while nc < width and grid_row[nc] == 5:
                end_col = nc
                nc += 1
            # Record the found segment
            length = end_col - start_col + 1
            segments.append({'start_col': start_col, 'end_col': end_col, 'length': length})
            # Move past the segment we just found
            c = end_col + 1
        else:
            # Not gray, move to the next pixel
            c += 1
    return segments

def transform(input_grid):
    """
    Transforms the input grid according to the described segment recoloring rules.

    Args:
        input_grid: A 2D numpy array, expected to be 1xN.

    Returns:
        A 2D numpy array representing the transformed grid.
    """
    # Ensure input is a 2D numpy array
    if not isinstance(input_grid, np.ndarray) or input_grid.ndim != 2:
         raise ValueError("Input must be a 2D numpy array")

    height, width = input_grid.shape

    # This task logic appears specific to 1-row grids based on examples
    if height != 1:
        # If grid has more than one row, behavior is undefined by examples.
        # Returning original grid or raising error are options.
        # For now, let's assume it only operates on the first row if multiple exist,
        # or just copy if it's not a 1xN grid that fits the pattern.
        # However, given ARC examples, we'll proceed assuming height is always 1.
        pass # Or raise ValueError("Transformation defined only for 1-row grids")

    # Initialize output grid as a copy of the input
    output_grid = np.copy(input_grid)
    grid_row = input_grid[0, :] # Work with the single row

    # 1. Identify all gray segments
    segments = find_gray_segments_1d(grid_row)
    num_segments = len(segments)

    # If no gray segments, return the original grid copy
    if num_segments == 0:
        return output_grid

    # 2. Determine the starting color based on total segment count
    # Odd count starts with 8 (azure), Even count starts with 9 (maroon)
    current_color = 8 if num_segments % 2 != 0 else 9

    previous_color = -1 # Placeholder for the first iteration
    previous_length_is_even = False

    # 3. Iterate through segments and assign colors
    for i, segment in enumerate(segments):
        start_col = segment['start_col']
        end_col = segment['end_col']
        length = segment['length']
        current_length_is_even = (length % 2 == 0)

        if i == 0:
            # First segment gets the calculated starting color
            pass # current_color is already set correctly
        else:
            # Subsequent segments: apply alternation logic
            # Check if both current and previous segments have even length
            if current_length_is_even and previous_length_is_even:
                # Rule Exception: Both even length -> retain previous color
                current_color = previous_color
            else:
                # Standard Rule: Alternate color
                current_color = 9 if previous_color == 8 else 8

        # 4. Recolor the segment in the output grid
        output_grid[0, start_col:end_col+1] = current_color

        # Update state for the next iteration
        previous_color = current_color
        previous_length_is_even = current_length_is_even

    return output_grid