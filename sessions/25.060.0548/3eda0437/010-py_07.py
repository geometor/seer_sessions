"""
Identify all horizontal segments of contiguous blue pixels in the input grid. 
For each blue segment, replace all the blue pixels in that segment with magenta 
pixels in the output grid, maintaining the same row and column positions.
"""

import numpy as np

def find_blue_segments(input_grid):
    """Finds all horizontal blue segments in the input grid."""
    blue_segments = []
    rows, cols = input_grid.shape
    for r in range(rows):
        in_blue_segment = False
        start_col = -1
        for c in range(cols):
            if input_grid[r, c] == 1:  # Blue pixel
                if not in_blue_segment:
                    in_blue_segment = True
                    start_col = c
            elif in_blue_segment:
                blue_segments.append(((r, start_col), (r, c - 1)))
                in_blue_segment = False
        if in_blue_segment:
            blue_segments.append(((r, start_col), (r, cols - 1)))
    return blue_segments

def transform(input_grid):
    """Transforms the input grid by replacing blue segments with magenta."""
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find all blue segments
    blue_segments = find_blue_segments(input_grid)

    # Replace each blue segment with magenta
    for start, end in blue_segments:
        row = start[0]
        start_col = start[1]
        end_col = end[1]
        output_grid[row, start_col:end_col+1] = 6

    return output_grid