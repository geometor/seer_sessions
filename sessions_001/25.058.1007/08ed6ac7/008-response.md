# 08ed6ac7 • 008 • refine_coder

---
```python
"""
1.  **Identify Gray Vertical Line Segments:** Scan the input grid to find all contiguous vertical line segments of gray (color 5) pixels.  A segment is one or more vertically adjacent gray pixels. Record the start and end position, and length of each segment.

2.  **Sort Segments by Length:** Sort the identified segments by their length in descending order (longest segment first).

3.  **Assign Colors Based on Rank:** Assign colors to the segments based on their sorted rank:
    *   Longest segment (rank 1): blue (color 1)
    *   Second longest segment (rank 2): red (color 2)
    *   Third longest segment (rank 3): green (color 3)
    *   Fourth longest segment (rank 4): yellow (color 4)
    *   All other segments: retain their original color (no change).

4.  **Transform Pixels:** Iterate through the pixels of each identified segment.  Replace the gray (color 5) with the assigned color based on the segment's rank. Pixels not part of a gray vertical segment remain unchanged.

5.  **Output:** Create an output grid with the transformed pixel colors.
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

    # Sort segments by length in descending order
    segment_lengths = [(seg, (seg[1][0] - seg[0][0] + 1)) for seg in gray_segments]
    sorted_segments = sorted(segment_lengths, key=lambda x: x[1], reverse=True)

    # Assign colors sequentially based on rank
    color_map = {
        0: 1,  # Rank 1: blue
        1: 2,  # Rank 2: red
        2: 3,  # Rank 3: green
        3: 4,   # Rank 4: yellow
    }

    # change output pixels
    for rank, (segment, length) in enumerate(sorted_segments):
        start, end = segment
        start_row, start_col = start
        end_row, end_col = end
        new_color = color_map.get(rank, 5) # Default to gray (5) - no change
        if new_color != 5: # only replace gray pixels
              for i in range(start_row, end_row + 1):
                output_grid[i, start_col] = new_color

    return output_grid
```
