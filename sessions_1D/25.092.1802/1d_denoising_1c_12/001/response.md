```python
import numpy as np
from typing import List, Dict, Tuple

# Color mapping (for reference, not used in logic)
COLOR_MAP = {
    0: (238, 238, 238),  # white
    1: (30, 147, 255),  # blue
    2: (220, 50, 40),  # red
    3: (79, 204, 48),  # green
    4: (230, 200, 0),  # yellow
    5: (85, 85, 85),  # gray
    6: (229, 58, 163),  # magenta
    7: (230, 120, 20),  # orange
    8: (135, 216, 241),  # azure
    9: (146, 18, 49),  # maroon
}

"""
Transforms the input grid by identifying the primary non-white color, finding the
longest continuous horizontal segment (run) of that color across all rows, and
creating an output grid containing only that longest segment against a white (0)
background. If multiple segments share the maximum length, the one in the topmost
row is selected.
"""

def find_segments_in_row(row: np.ndarray, color: int) -> List[Dict[str, int]]:
    """
    Finds all continuous horizontal segments of a given color in a single row.

    Args:
        row: A 1D numpy array representing a row of the grid.
        color: The target color integer to find segments of.

    Returns:
        A list of dictionaries, where each dictionary represents a segment
        and contains 'start' (column index), 'end' (column index), and 'len' (length).
        Returns an empty list if no segments of the specified color are found.
    """
    segments = []
    start_col = -1
    row_len = len(row)
    for c, pixel in enumerate(row):
        # Start of a new segment
        if pixel == color and start_col == -1:
            start_col = c
        # End of the current segment (pixel color changed or still same color but start_col is set)
        elif pixel != color and start_col != -1:
            segments.append({'start': start_col, 'end': c - 1, 'len': c - start_col})
            start_col = -1 # Reset for next potential segment

    # Handle a segment that extends to the very end of the row
    if start_col != -1:
        segments.append({'start': start_col, 'end': row_len - 1, 'len': row_len - start_col})

    return segments

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation logic to find and isolate the longest horizontal
    segment of the primary non-white color.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the output grid.
    """
    # Convert input to numpy array for easier processing
    input_np = np.array(input_grid, dtype=int)

    # Initialize output grid with the same shape, filled with background color (0)
    output_grid = np.zeros_like(input_np)
    rows, cols = input_np.shape

    # Identify the primary non-white color in the grid
    # We assume there is at most one dominant non-white color based on examples
    primary_color = 0
    unique_colors = np.unique(input_np)
    for color in unique_colors:
        if color != 0:
            primary_color = color
            break

    # If the grid is entirely white or no non-white color is found, return the empty grid
    if primary_color == 0:
        return output_grid.tolist()

    # Variables to store information about the longest segment found so far
    max_len = 0
    # Stores {'row': r, 'start': start_col, 'end': end_col}
    best_segment_info = None

    # Iterate through each row to find all horizontal segments of the primary color
    for r in range(rows):
        # Find all segments of the primary color in the current row
        row_segments = find_segments_in_row(input_np[r, :], primary_color)

        # Check if any segment in this row is longer than the current max
        for segment in row_segments:
            # If current segment is strictly longer, it becomes the new best
            if segment['len'] > max_len:
                max_len = segment['len']
                best_segment_info = {'row': r, 'start': segment['start'], 'end': segment['end']}
            # Tie-breaking: if lengths are equal, we prefer the segment in the topmost row.
            # Since we iterate row by row from top (r=0), an equal length segment found
            # later (larger 'r') will not replace the existing 'best_segment_info'.

    # If a longest segment was found, draw it onto the output grid
    if best_segment_info is not None:
        r = best_segment_info['row']
        start_col = best_segment_info['start']
        end_col = best_segment_info['end'] # end_col is inclusive

        # Fill the pixels of the longest segment in the output grid
        for c in range(start_col, end_col + 1):
             output_grid[r, c] = primary_color

    # Convert the numpy array back to a list of lists before returning
    return output_grid.tolist()
```