"""
1.  **Identify Top Row Pattern:** Examine the first row (top row) of the input grid. Note the colors and their order, excluding any azure (8) pixels. This is the "top row pattern".

2.  **Row Matching:** Iterate through each row of the input grid.

3.  **Conditional Row Transformation and Copying Unchanged Rows:**
    *   Compare the non-azure colors of the current row with the "top row pattern".
    *   If the row *exactly matches* the top row pattern (excluding azure pixels), replace the entire row in the output grid with a *copy* of the top row of the input grid (including azure pixels). Then, propagate the non-azure colors in that copied row downwards.
        - **Propagation:** For each non-azure pixel in the transformed row, copy its value downwards through all subsequent rows in the output grid, within the same column. If the pixel in the same column is transformed later, the later transformation overwrites the previous value.
    * If the row *does not match* the top row pattern, find segments where non-azure pixels *do not change* as compared with the row directly above. Propagate these colors *downward* within their segment, but only until a matched row is encountered.

4. **Handling of Azures (8):** Azure pixels in the input should appear where present in any matched row. Azure pixels in unmatched rows do not vertically propagate.
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

            # 4. Segment-Based Propagation (Matched Rows)
            segments = get_segments(transformed_row)
            for value, start_x, length in segments:
                if value != 8:  # Non-azure segment
                    for x in range(start_x, start_x + length):
                        for row_below in range(y + 1, height):
                            output_grid[row_below, x] = value
            output_grid[y] = transformed_row  # set transformed row
        else:
            # Handle unmatched rows: propagate unchanged non-azure segments down
            if y > 0: # propagation starts from 2nd row
                prev_row = input_grid[y-1]
                curr_row = input_grid[y]
                for x in range(width):
                    if curr_row[x] != 8 and curr_row[x] == prev_row[x]:
                       # propagate downwards until matched row or end
                       for row_below in range(y+1, height):
                           below_row_pattern = get_non_azure_pattern(input_grid[row_below])
                           if np.array_equal(below_row_pattern, top_row_pattern):
                               break # stop propagation if a matched row
                           output_grid[row_below, x] = curr_row[x]

    return output_grid.tolist()