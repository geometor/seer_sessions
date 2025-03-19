"""
1.  **Identify Vertical Line Segments:** Scan the input grid to find all contiguous vertical line segments of gray (color 5) pixels. A segment is defined as one or more vertically adjacent gray pixels. The length and position of each segment should be recorded.

2.  **Order Segments:** Sort the identified segments based on their horizontal position (column index) from left to right.

3.  **Assign Colors:** Assign a unique color to each segment based on its order:
    *   The leftmost segment receives color 1 (blue).
    *   The second segment from the left receives color 2 (red).
    *   The third segment receives color 3 (green).
    *   The fourth segment receives color 4 (yellow).
    *   If there are more than four segments, any additional segment will not change color.

4.  **Transform:** For each identified segment, iterate through its pixels and replace the gray (5) color with the assigned color. Pixels that are not part of a gray vertical segment are not modified.

5.  **Output:** Create the output grid containing the transformed pixels.
"""

import numpy as np

def find_vertical_segments(grid, color):
    """Finds all contiguous vertical line segments of a specified color."""
    segments = []
    rows, cols = grid.shape
    for j in range(cols):
        in_segment = False
        start_row = -1
        for i in range(rows):
            if grid[i, j] == color:
                if not in_segment:
                    in_segment = True
                    start_row = i
            elif in_segment:
                in_segment = False
                segments.append(((start_row, j), (i - 1, j)))  # (start, end)
                start_row = -1
        if in_segment:  # Handle segment at the end of the column
            segments.append(((start_row, j), (rows - 1, j)))
    return segments

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # Find vertical line segments of gray (5) pixels
    gray_segments = find_vertical_segments(input_grid, 5)

    # Sort segments by column (x-coordinate of start point)
    sorted_segments = sorted(gray_segments, key=lambda seg: seg[0][1])

    # Assign colors sequentially
    color_map = {
        0: 1,  # First segment: blue
        1: 2,  # Second segment: red
        2: 3,  # Third segment: green
        3: 4,   # Fourth segment: yellow
    }

    # change output pixels
    for index, segment in enumerate(sorted_segments):
        start, end = segment
        start_row, start_col = start
        end_row, end_col = end
        new_color = color_map.get(index, 0) # Default to white (0) if index is out of range
        if new_color != 0:
             for i in range(start_row, end_row + 1):
                 output_grid[i, start_col] = new_color

    return output_grid