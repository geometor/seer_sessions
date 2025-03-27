"""
1.  **Preserve Boundaries:** The top and bottom rows of the input grid remain unchanged in the output grid.

2.  **Inner Row Transformation:** For each row from the second row to the second-to-last row:
    *   Iterate through the row from left to right.
    *   Identify contiguous segments of pixels with the same color.
    *   For each segment:
        * Check if there is space available to the left (the segment is *not* at the beginning of the row).
        *   If the left adjacent pixel has different color AND there is at least one pixel with a different color to the right of the segment:
            *   Shift every pixel within the segment to the left by one position.
            *   The vacated position to the far right of the shifted segment will now contain the value immediately to the right of the original segment.
            *   After each shift within the same row, recheck from the start index of the originally shifted segment for any further left shift possibilities in case the current segment needs to be shifted more than once.
    * If no different color exists to the right of the segment (all values to the right until the end of row are the same color) do not shift.

3. Repeat Step 2 for every inner row.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the observed rule."""
    rows, cols = input_grid.shape
    output_grid = np.copy(input_grid)

    # Iterate through inner rows
    for i in range(1, rows - 1):
        j = 0
        while j < cols:
            # Find consecutive same-color segments
            start = j
            while j + 1 < cols and input_grid[i, j] == input_grid[i, j + 1]:
                j += 1
            end = j

            # Check for shifting conditions
            while True:
                if start > 0 and input_grid[i, start-1] != input_grid[i, start] and end + 1 < cols:
                    #Different color exists on the right side
                    
                    # Shift the segment to the left
                    for k in range(start, end + 1):
                        output_grid[i, k - 1] = input_grid[i, k]
                    output_grid[i, end] = input_grid[i, end + 1]
                    start -= 1
                    end -= 1
                else:
                  break

            j = end + 1

    return output_grid