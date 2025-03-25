"""
The transformation rule creates a 2x2 output grid. The color of the output grid is determined by comparing the maximum length of contiguous vertical segments of red (2) and yellow (4) pixels in the input grid. If the longest red segment is greater than or equal to the longest yellow segment, the output grid is filled with red (2). Otherwise, the output grid is filled with yellow (4).
"""

import numpy as np

def find_vertical_segments(grid):
    """Finds vertical segments of colors 2 (red) and 4 (yellow) and returns their lengths and column indices."""
    rows, cols = grid.shape
    segments = {2: [], 4: []}
    for c in range(cols):
        count_2 = 0
        count_4 = 0
        for r in range(rows):
            if grid[r, c] == 2:
                count_2 += 1
                if count_4 > 0:
                  segments[4].append(count_4)
                  count_4 = 0
            elif grid[r, c] == 4:
                count_4 += 1
                if count_2 > 0:
                    segments[2].append(count_2)
                    count_2 = 0
            else:
                if count_2 > 0:
                    segments[2].append(count_2)
                    count_2 = 0
                if count_4 > 0:
                  segments[4].append(count_4)
                  count_4 = 0
        if count_2 > 0:
            segments[2].append(count_2)
        if count_4 > 0:
            segments[4].append(count_4)
    return segments

def transform(input_grid):
    """Transforms the input grid to a 2x2 grid based on the longest vertical segments of red and yellow."""
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.zeros((2, 2), dtype=int)

    # Find vertical segments of color 2 (red) and 4 (yellow).
    segments = find_vertical_segments(input_grid)

    # Determine the output color based on the maximum segment lengths.
    max_len_2 = 0
    if len(segments[2]) > 0:
      max_len_2 = max(segments[2])

    max_len_4 = 0
    if len(segments[4]) > 0:
      max_len_4 = max(segments[4])

    if max_len_2 >= max_len_4 and max_len_2 > 0:
        output_color = 2
    elif max_len_4 > max_len_2:
        output_color = 4
    else:
        output_color = 0  # Default to black if no red or yellow

    # change output pixels
    output_grid[:] = output_color

    return output_grid