"""
1.  **Identify the Top Row Pattern:** Examine the first row (the top row) of the input grid. Note the colors and their order, excluding any azure (8) pixels. This forms the "top row pattern".
2.  **Row Matching:** Iterate through each row of the input grid (excluding the top row itself).
3.  **Conditional Row Transformation**: For each row:
    - Compare the colors of the current row (excluding azure pixels), with the "top row pattern" (also excluding azure).
    - If the non-azure colors of the current row exactly match the top row non-azure pattern, the row is eligible for transformation.

4.  **Segment-Based Propagation:** Within each *transformed* row:
    - Identify segments. A segment is defined as consecutive pixels of same value.
    - Iterate over the segments. For segments that are *not* azure:
       - For each non-azure pixel in the segment, copy its value downwards through all subsequent rows in the output grid, within the same column. If the pixel in same column is transformed later, it overwrites the previous value.
5.  **Preserve Unmatched Rows**: If a row in the input grid does *not* match the top row pattern (excluding azure pixels), it is copied to the output grid *unchanged*.
"""

import numpy as np

def get_non_azure_pattern(row):
    """Extracts the non-azure pattern from a row."""
    return row[row != 8]

def get_segments(row):
    """Identifies segments in row"""
    segments = []
    if not row.size:  # Handle empty rows
        return segments

    current_segment = [row[0]]
    for i in range(1, len(row)):
        if row[i] == current_segment[-1]:
            current_segment.append(row[i])
        else:
            segments.append((current_segment[-1], len(current_segment))) # value, length
            current_segment = [row[i]]
    segments.append((current_segment[-1], len(current_segment))) # Append the last segment

    # Return segment starting positions
    segment_positions = []
    current_pos = 0
    for value, length in segments:
        segment_positions.append( (value, current_pos, length) )
        current_pos += length
    return segment_positions

def transform(input_grid):
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # 1. Identify Top Row Pattern
    top_row_pattern = get_non_azure_pattern(input_grid[0])

    # 2. & 3. Row Matching and Conditional Transformation
    for y in range(height):
        current_row_pattern = get_non_azure_pattern(input_grid[y])
        if np.array_equal(current_row_pattern, top_row_pattern):
            # Transform the row to match top row (including azures).
            transformed_row = np.copy(input_grid[0])

            # 4. Segment-Based Propagation
            segments = get_segments(transformed_row)
            for value, start_x, length in segments:
                if value != 8:  # Non-azure segment
                    for x in range(start_x,start_x + length):
                        for row_below in range(y + 1, height):
                            output_grid[row_below, x] = value
            output_grid[y] = transformed_row # set transformed row

    return output_grid.tolist()