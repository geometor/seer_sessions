# 3bdb4ada • 008 • refine_coder

---
```python
"""
1.  **Identify Rectangles:** Locate all horizontal rectangular blocks of uniform color within the input grid, *where the height of the rectangle is greater than 1*.
2.  **Target Middle Row:** For each identified rectangle, locate its middle row.
3.  **Apply Checkerboard Pattern:**  Within the middle row, starting from the leftmost pixel of the rectangle on that row, alternate the pixel colors between the rectangle's original color and white (0).
4. **Preserve other Pixels:** All pixels not within a valid rectangle identified in Step 1 are kept unchanged from the input grid.
"""

import numpy as np

def find_rectangles(grid):
    # Find contiguous horizontal blocks of the same color with height > 1
    rectangles = []
    rows, cols = grid.shape
    for r in range(rows):
        start_col = None
        current_color = None
        for c in range(cols):
            if start_col is None:
                start_col = c
                current_color = grid[r, c]
            elif grid[r, c] != current_color:
                if current_color != 0:  # Ignore white background
                    # Calculate height
                    height = 1
                    for r2 in range(r + 1, rows):
                        if grid[r2, start_col] == current_color:
                            height +=1
                        else:
                            break
                    if height > 1:
                        rectangles.append(((r, start_col), (r + height -1, c - 1), current_color))
                start_col = c
                current_color = grid[r, c]
        if start_col is not None and current_color != 0:
            # Calculate height for the last block
            height = 1
            for r2 in range(r + 1, rows):
                if grid[r2, start_col] == current_color:
                  height += 1
                else:
                  break;
            if height > 1:
                rectangles.append(((r, start_col), (r+ height-1, cols - 1), current_color))
    return rectangles

def transform(input_grid):
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find rectangles
    rectangles = find_rectangles(input_grid)

    # Iterate through rectangles and apply checkerboard pattern to the middle row
    for rect in rectangles:
        start, end, color = rect
        start_row, start_col = start
        end_row, end_col = end

        mid_row = start_row + (end_row - start_row) // 2

        # Apply checkerboard pattern
        for c in range(start_col, end_col + 1):
            if (c - start_col) % 2 == 1:
                output_grid[mid_row, c] = 0

    return output_grid
```
