"""
1.  **Preserve Boundaries:** The first (top) and last (bottom) rows of the input grid remain unchanged in the output grid.

2.  **Inner Row Transformation:**  For each row from the second row to the second-to-last row:

3.  **Conditional Left Shift:** Starting from the leftmost pixel examine if its immediate right value. If it is equal, skip to the next. However, examine the pixels to the right. If consecutive pixels share the same color and the sequence is followed by a different color, the entire segment with the same color *shifts* one position to the left, only if the cell to the left is of a different color and is *not* part of an unchanged row. The "different color" pixel on the right of the same-color sequence effectively acts as a boundary, blocking a shift beyond it.

4. If a series of repeating colors extends until the last column, no shift is applied and it remains unchanged.
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

            # Check for a different color boundary on the right and available space to the left
            if end + 1 < cols and start > 0 and input_grid[i, start-1] != input_grid[i,start]: # and input_grid[i, end] != input_grid[i,end+1]:
                # Shift the segment to the left
                for k in range(start, end + 1):
                    output_grid[i, k - 1] = input_grid[i, k]
                # Check if series reached the end before shift
                if end+1 != cols:
                  output_grid[i, end] = input_grid[i,end+1] # boundary color

            j = end + 1  # Move to the next segment

    return output_grid