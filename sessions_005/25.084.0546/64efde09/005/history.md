
Previous Code:
```python
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
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 4 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 4 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 3 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 3 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 3 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 3 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 4 8 8 8 8 8 8 8 8 8
8 4 3 3 3 3 4 4 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 2 2 2 2 2 2 4 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 4 3 3 3 3 4 4 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 2 2 2 2 2 2 4 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 4 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 2 8 8 8 8 6
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 3 2 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 3 2 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 3 2 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 3 2 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 2 8 8 8 8 8
8 8 8 5 8 8 8 8 8 8 8 8 8 1 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```
Expected Output:
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 4 8 8 8 8 8 8 8 8 8
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 2 4 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 3 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 3 8 8 8 8 8 8 8 8 8
5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 2 3 8 8 8 8 8 8 8 8 8
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2 3 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 4 8 8 8 8 8 8 8 8 8
8 4 3 3 3 3 4 4 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 2 2 2 2 2 2 4 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 1 5 8 8 6 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 1 5 8 8 6 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 1 5 8 8 6 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 1 5 8 8 6 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 1 5 8 8 6 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 1 5 8 8 6 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 1 5 8 8 6 8 8 8 8 8 4 3 3 3 3 4 4 8 8 8 8 8 8 8 8 8 8
8 8 1 5 8 8 6 8 8 8 8 8 2 2 2 2 2 2 4 8 8 8 8 8 8 8 8 8 8
8 8 1 5 8 8 6 8 8 8 8 8 8 1 5 8 8 6 8 8 8 8 8 8 8 8 8 8 8
8 8 1 5 8 8 6 8 8 8 8 8 8 1 5 8 8 6 8 8 8 8 4 4 8 8 8 8 8
8 8 1 5 8 8 6 8 8 8 8 8 8 1 5 8 8 6 8 8 8 8 4 2 6 6 6 6 6
8 8 1 5 8 8 6 8 8 8 8 8 8 1 5 8 8 6 8 8 8 8 3 2 8 8 8 8 8
8 8 1 5 8 8 6 8 8 8 8 8 8 1 5 8 8 6 8 8 8 8 3 2 8 8 8 8 8
8 8 1 5 8 8 6 8 8 8 8 8 8 1 5 8 8 6 8 8 8 8 3 2 5 5 5 5 5
8 8 1 5 8 8 6 8 8 8 8 8 8 1 5 8 8 6 8 8 8 8 3 2 1 1 1 1 1
8 8 1 5 8 8 6 8 8 8 8 8 8 1 5 8 8 6 8 8 8 8 4 2 8 8 8 8 8
8 8 1 5 8 8 6 8 8 8 8 8 8 1 5 8 8 6 8 8 8 8 8 8 8 8 8 8 8
```
Transformed Output:
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 4 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 4 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 4 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 4 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 4 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 4 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 4 8 8 8 8 8 8 8 8 8
8 4 3 3 3 3 4 4 8 8 8 8 8 8 8 8 8 8 4 4 8 8 8 8 8 8 8 8 8
8 2 2 2 2 2 2 4 8 8 8 8 8 8 8 8 8 8 4 4 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 4 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 4 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 4 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 4 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 4 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 4 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 4 3 3 3 3 4 4 4 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 2 2 2 2 2 2 4 4 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 4 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 4 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 4 8 8 4 2 8 8 8 8 6
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 4 8 8 3 2 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 4 8 8 3 2 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 4 8 8 3 2 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 4 8 8 3 2 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 4 8 8 4 2 8 8 8 8 8
8 8 8 5 8 8 8 8 8 8 8 8 8 1 8 8 8 8 4 4 8 8 8 8 8 8 8 8 8
```
Match: False
Pixels Off: 192
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 50.928381962864705

## Example 2:
Input:
```
8 8 8 8 8 1 4 8 8 8 8 8 8 8 8 8 8 8 8 6 8 8 8 8 8 8 8
3 8 8 8 8 1 4 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 1 2 8 8 8 8 8 8 8 1 1 1 1 1 1 1 1 1 8 8 8 8
8 8 8 8 8 1 2 8 8 8 8 8 8 8 4 2 2 2 2 2 2 4 4 8 8 8 8
8 8 8 8 8 1 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
9 8 8 8 8 1 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 1 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 1 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 1 4 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 1 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 1 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 1 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 1 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 1 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 1 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 1 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 1 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 1 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```
Expected Output:
```
8 8 8 8 8 1 4 8 8 8 8 8 8 8 8 8 8 9 8 6 8 3 8 8 8 8 8
3 3 3 3 3 1 4 8 8 8 8 8 8 8 8 8 8 9 8 6 8 3 8 8 8 8 8
8 8 8 8 8 1 2 8 8 8 8 8 8 8 1 1 1 1 1 1 1 1 1 8 8 8 8
6 6 6 6 6 1 2 8 8 8 8 8 8 8 4 2 2 2 2 2 2 4 4 8 8 8 8
8 8 8 8 8 1 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
9 9 9 9 9 1 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 1 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 1 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 1 4 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 1 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 1 3 3 3 3 3 3 3 3 3
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 1 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 1 6 6 6 6 6 6 6 6 6
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 1 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 1 9 9 9 9 9 9 9 9 9
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 1 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 1 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 1 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```
Transformed Output:
```
8 8 8 8 8 1 4 8 8 8 8 8 8 8 8 8 8 8 8 6 8 8 8 8 8 8 8
3 8 8 8 8 1 4 8 8 8 8 8 8 8 8 8 8 8 8 6 8 8 8 8 8 8 8
8 8 8 8 8 1 4 8 8 8 8 8 8 8 1 1 1 1 1 6 1 1 1 8 8 8 8
8 8 8 8 8 1 4 8 8 8 8 8 8 8 4 2 2 2 2 6 2 4 4 8 8 8 8
8 8 8 8 8 1 4 8 8 8 8 8 8 8 8 8 8 8 8 6 8 8 8 8 8 8 8
9 8 8 8 8 1 4 8 8 8 8 8 8 8 8 8 8 8 8 6 8 8 8 8 8 8 8
8 8 8 8 8 1 4 8 8 8 8 8 8 8 8 8 8 8 8 6 8 8 8 8 8 8 8
8 8 8 8 8 1 4 8 8 8 8 8 8 8 8 8 8 8 8 6 8 8 8 8 8 8 8
8 8 8 8 8 1 4 8 8 8 8 8 8 8 8 8 8 8 8 6 8 8 8 8 8 8 8
8 8 8 8 8 1 4 8 8 8 8 8 8 8 8 8 4 1 8 6 8 8 8 8 8 8 8
8 8 8 8 8 1 4 8 8 8 8 8 8 8 8 8 4 1 8 6 8 8 8 8 8 8 8
8 8 8 8 8 1 4 8 8 8 8 8 8 8 8 8 2 1 8 6 8 8 8 8 8 8 8
8 8 8 8 8 1 4 8 8 8 8 8 8 8 8 8 2 1 8 6 8 8 8 8 8 8 8
8 8 8 8 8 1 4 8 8 8 8 8 8 8 8 8 2 1 8 6 8 8 8 8 8 8 8
8 8 8 8 8 1 4 8 8 8 8 8 8 8 8 8 2 1 8 6 8 8 8 8 8 8 8
8 8 8 8 8 1 4 8 8 8 8 8 8 8 8 8 2 1 8 6 8 8 8 8 8 8 8
8 8 8 8 8 1 4 8 8 8 8 8 8 8 8 8 2 1 8 6 8 8 8 8 8 8 8
8 8 8 8 8 1 4 8 8 8 8 8 8 8 8 8 4 1 8 6 8 8 8 8 8 8 8
8 8 8 8 8 1 4 8 8 8 8 8 8 8 8 8 8 8 8 6 8 8 8 8 8 8 8
8 8 8 8 8 1 4 8 8 8 8 8 8 8 8 8 8 8 8 6 8 8 8 8 8 8 8
8 8 8 8 8 1 4 8 8 8 8 8 8 8 8 8 8 8 8 6 8 8 8 8 8 8 8
```
Match: False
Pixels Off: 89
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 31.393298059964735
Okay, let's analyze the provided information and develop a strategy to improve the transformation rule and the corresponding code.

**General Assessment:**

The initial natural language program and code were based on observations from the first training example. The tests on the two examples reveal significant discrepancies between the transformed output and the expected output. This indicates that the initial rule is too simplistic and doesn't capture the full complexity of the transformation. The primary issue appears to be an incorrect application of the segment propagation. The initial rule copies *only* the first row and propagates those segments that aren't azure, which works if there is an initial pattern match. However, it isn't correctly handling the cases of rows which are not matched. It also fails to account for all cases in the vertical propagation in the second example.

**Strategy for Resolving Errors:**

1.  **Detailed Example Analysis:** Carefully examine each input-output pair, paying close attention to:
    *   Rows that match the top row pattern.
    *   Rows that *don't* match the top row pattern.
    *   How colors propagate vertically, especially in unmatched rows. It appears there will be cases where unmatched rows should be copied unchanged.
    *   Edge cases or unusual patterns.

2.  **Refine the Natural Language Program:** Based on the detailed analysis, update the natural language program to accurately describe the transformation logic. We'll pay special attention to:
    *   Clarifying the conditions for row transformation.
    *   Defining the vertical propagation rules precisely.
    *   Addressing how unmatched rows are handled.

3.  **Iterative Code Modification:** Modify the Python code to reflect the refined natural language program. Test the updated code after each significant change.

4.  **Metrics:** Use tool use to get additional insight to the example outputs, for example to determine what the matching and non-matching rows are.

**Metrics Gathering (using tool_code):**

Let's gather some metrics to understand the transformations better. I'll focus on identifying matching and non-matching rows in both examples.



*code_execution:*
```python
import numpy as np

def get_non_azure_pattern(row):
    """Extracts the non-azure pattern from a row."""
    return row[row != 8]

def analyze_example(input_grid, expected_output):
    input_grid = np.array(input_grid)
    expected_output = np.array(expected_output)
    height, width = input_grid.shape

    top_row_pattern = get_non_azure_pattern(input_grid[0])
    matching_rows = []
    non_matching_rows = []

    for y in range(height):
        current_row_pattern = get_non_azure_pattern(input_grid[y])
        if np.array_equal(current_row_pattern, top_row_pattern):
            matching_rows.append(y)
        else:
            non_matching_rows.append(y)

    print(f"Top Row Pattern: {top_row_pattern}")
    print(f"Matching Rows: {matching_rows}")
    print(f"Non-Matching Rows: {non_matching_rows}")

# Example 1 Data
input_grid_1 = [
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 4, 4, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 2, 4, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 2, 3, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 2, 3, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 2, 3, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 2, 3, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 2, 4, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 4, 3, 3, 3, 3, 4, 4, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 2, 2, 2, 2, 2, 2, 4, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 4, 3, 3, 3, 3, 4, 4, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 2, 2, 2, 2, 2, 2, 4, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 4, 4, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 4, 2, 8, 8, 8, 8, 6],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 3, 2, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 3, 2, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 3, 2, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 3, 2, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 4, 2, 8, 8, 8, 8, 8],
    [8, 8, 8, 5, 8, 8, 8, 8, 8, 8, 8, 8, 8, 1, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]
]

# Example 2 Data
input_grid_2 = [
   [8, 8, 8, 8, 8, 1, 4, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 6, 8, 8, 8, 8, 8, 8, 8],
   [3, 8, 8, 8, 8, 1, 4, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
   [8, 8, 8, 8, 8, 1, 2, 8, 8, 8, 8, 8, 8, 8, 1, 1, 1, 1, 1, 1, 1, 1, 1, 8, 8, 8, 8],
   [8, 8, 8, 8, 8, 1, 2, 8, 8, 8, 8, 8, 8, 8, 4, 2, 2, 2, 2, 2, 2, 4, 4, 8, 8, 8, 8],
   [8, 8, 8, 8, 8, 1, 2, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
   [9, 8, 8, 8, 8, 1, 2, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
   [8, 8, 8, 8, 8, 1, 2, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
   [8, 8, 8, 8, 8, 1, 2, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
   [8, 8, 8, 8, 8, 1, 4, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
   [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 4, 1, 8, 8, 8, 8, 8, 8, 8, 8, 8],
   [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 4, 1, 8, 8, 8, 8, 8, 8, 8, 8, 8],
   [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 2, 1, 8, 8, 8, 8, 8, 8, 8, 8, 8],
   [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 2, 1, 8, 8, 8, 8, 8, 8, 8, 8, 8],
   [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 2, 1, 8, 8, 8, 8, 8, 8, 8, 8, 8],
   [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 2, 1, 8, 8, 8, 8, 8, 8, 8, 8, 8],
   [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 2, 1, 8, 8, 8, 8, 8, 8, 8, 8, 8],
   [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 2, 1, 8, 8, 8, 8, 8, 8, 8, 8, 8],
   [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 4, 1, 8, 8, 8, 8, 8, 8, 8, 8, 8],
   [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
   [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
   [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]
]
print("Example 1:")
analyze_example(input_grid_1, [])
print("\nExample 2:")
analyze_example(input_grid_2, [])


```

*code_execution_result:*
outcome: 1
```
Example 1:
Top Row Pattern: [4 4]
Matching Rows: [0, 18]
Non-Matching Rows: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 19, 20, 21, 22, 23, 24, 25]

Example 2:
Top Row Pattern: [1 4 6]
Matching Rows: [0]
Non-Matching Rows: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

```
**YAML Documentation:**


```yaml
example_1:
  objects:
    - id: top_row
      type: row
      properties:
        pattern: [4, 4]  # Non-azure values
    - id: matching_rows
      type: list
      properties:
          indexes: [0, 18]
    - id: non_matching_rows
      type: list
      properties:
        indexes: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 19, 20, 21, 22, 23, 24, 25]
    - id: grid
      type: 2D array
      properties:
        height: 26
        width: 29
  actions:
    - name: match_pattern
      description: Compare row pattern to top row pattern.
    - name: propagate_color
      description: Copy color downwards if row matches.

example_2:
  objects:
    - id: top_row
      type: row
      properties:
        pattern: [1, 4, 6] # Non-azure values
    - id: matching_rows
      type: list
      properties:
        indexes: [0]
    - id: non_matching_rows
      type: list
      properties:
          indexes: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    - id: grid
      type: 2D array
      properties:
        height: 21
        width: 27
  actions:
    - name: match_pattern
      description: Compare row pattern to top row pattern.
    - name: propagate_color
      description: Copy color downwards if the row matches top row.

```


**Refined Natural Language Program:**

1.  **Identify Top Row Pattern:** Examine the first row (top row) of the input grid. Note the colors and their order, excluding any azure (8) pixels. This is the "top row pattern".

2.  **Row Matching:** Iterate through each row of the input grid.

3.  **Conditional Row Transformation and Copying Unchanged Rows:**
    *   Compare the non-azure colors of the current row with the "top row pattern".
    *   If the row *exactly matches* the top row pattern (excluding azure pixels), replace the entire row in the output grid with a *copy* of the top row of the input grid (including azure pixels). Then, propagate the non-azure colors in that copied row downwards.
        - **Propagation:** For each non-azure pixel in the transformed row, copy its value downwards through all subsequent rows in the output grid, within the same column. If the pixel in the same column is transformed later, the later transformation overwrites the previous value.
    * If the row *does not match* the top row pattern, find segments where non-azure pixels *do not change* as compared with the row directly above. Propagate these colors *downward* within their segment, but only until a matched row is encountered.

4. **Handling of Azures (8):** Azure pixels in the input should appear where present in any matched row. Azure pixels in unmatched rows do not vertically propagate.

