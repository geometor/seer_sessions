"""
1.  **Iterate through Rows:** Examine each row in the input grid.
2.  **Identify Segments:** Within each row, identify segments that meet these criteria:

    *   The segment starts and ends with the *same* non-zero color.
    *   All pixels between the start and end are '0' (white).
3.  **Fill Segments:** If a segment is found, replace all '0' (white) pixels *within that segment* with the color of the segment's start/end pixels.
4. **Other Pixels**: Pixels that aren't the segment defined above maintain their original values.
"""

import numpy as np

def find_segments(row):
    """Finds segments within a row that meet the specified criteria."""
    segments = []
    start = -1
    for i, pixel in enumerate(row):
        if pixel != 0:
            if start == -1:
                start = i
            else:
                # Check if segment is valid (all 0s in between and same color)
                if row[start] == pixel and all(row[j] == 0 for j in range(start + 1, i)):
                    segments.append((start, i, pixel))  # Store start, end, and color
                start = i  # Reset start for the next potential segment
    return segments

def transform(input_grid):
    """Transforms the input grid according to the specified rule."""
    output_grid = np.copy(input_grid)  # Initialize output_grid as a copy
    rows, _ = input_grid.shape

    for i in range(rows):
        # Find segments in the current row
        segments = find_segments(input_grid[i])

        # Fill the identified segments
        for start, end, color in segments:
            output_grid[i, start:end+1] = color

    return output_grid