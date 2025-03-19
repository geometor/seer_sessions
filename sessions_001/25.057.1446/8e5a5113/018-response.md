# 8e5a5113 • 018 • refine_coder

---
```python
"""
The transformation involves identifying a "pivot" of gray (5) and optionally white (0) pixels in each row of the input grid. The area to the left of the gray(5) is reflected to the right of the pivot, and the area to the right of the pivot (including the white pixels) is mirrored to the left. The output grid has the same dimensions as the input.
"""

import numpy as np

def find_pivot(row):
    """
    Finds the start and end indices of the pivot in a given row.

    Args:
        row: A 1D numpy array representing a row of the grid.

    Returns:
        A tuple (start, end) where 'start' is the index of the first gray (5)
        pixel, and 'end' is the index of the last pixel of the pivot (either gray or white).
        Returns (None, None) if no pivot is found.
    """
    gray_indices = np.where(row == 5)[0]
    if gray_indices.size == 0:
        return None, None

    start = gray_indices[0]
    end = start
    for i in range(start + 1, len(row)):
        if row[i] == 5:
            end = i
        elif row[i] == 0:
            end = i
        else:
            break
    return start, end


def transform(input_grid):
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    for row_index in range(rows):
        row = input_grid[row_index]
        pivot_start, pivot_end = find_pivot(row)

        if pivot_start is not None:
            # Reflect Left to Right
            left_side = row[:pivot_start]
            reflect_len = len(left_side)
            right_start = pivot_end + 1

            for i in range(reflect_len):
                dest_index = right_start + i
                if dest_index < cols:
                     output_grid[row_index, dest_index] = left_side[reflect_len - 1 - i]
                
            # Mirror Right to Left
            right_side = row[pivot_end + 1:]
            mirror_len = len(right_side)

            for i in range(mirror_len):
                dest_index = pivot_start - 1 - i
                if dest_index >= 0:
                    output_grid[row_index, dest_index] = right_side[i]

    return output_grid
```
