# db3e9e38 • 006 • refine_coder

---
```python
"""
1.  **Identify the Vertical Line:** Locate the longest contiguous vertical line of orange (7) pixels within the input grid. Note its starting row, ending row, and column index.

2.  **Construct the Vertical Component:** The output grid will include the original orange vertical line, unchanged.

3.  **Construct the Horizontal Arms:** For each row that contains the vertical orange line:
    *   Place an azure (8) pixel immediately to the left and right of the orange pixel.
    *    From each of those azure pixels, extend outwards toward the edges of the grid, maintaining the correct color for the pixel, skipping any 'white' background pixels.

4.  **Preserve Background:** Ensure that all pixels in the input grid, *except* those involved in forming the cross, are copied to the output grid without modification. The 'white' background should not impact the color of the arms.
"""

import numpy as np

def find_vertical_line(grid, color):
    rows, cols = grid.shape
    for j in range(cols):
        for i in range(rows):
            if grid[i, j] == color:
                # Check for contiguous vertical line
                start_row = i
                end_row = i
                while end_row + 1 < rows and grid[end_row + 1, j] == color:
                    end_row += 1
                length = end_row - start_row + 1
                return start_row, end_row, j, length  # Return line info
    return None, None, None, None

def transform(input_grid):
    # Initialize output grid with the same values as the input grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find the vertical orange line
    start_row, end_row, col_index, length = find_vertical_line(input_grid, 7)

    if start_row is not None:
        # Construct the horizontal arms, skipping white pixels
        for row_index in range(start_row, end_row + 1):
            # Place azure pixels next to the orange pixel
            if col_index > 0:
              if output_grid[row_index,col_index - 1]!=0:
                output_grid[row_index, col_index - 1] = 8
            if col_index < cols - 1:
                if output_grid[row_index,col_index + 1]!=0:
                  output_grid[row_index, col_index + 1] = 8

            # Extend left, skipping white pixels
            color = 8
            for c in range(col_index - 1, -1, -1):
                if output_grid[row_index, c] != 0:
                    output_grid[row_index, c] = color
                    color = 7 if color == 8 else 8

            # Extend right, skipping white pixels
            color = 8
            for c in range(col_index + 1, cols):
                if output_grid[row_index, c] != 0:
                    output_grid[row_index, c] = color
                    color = 7 if color == 8 else 8
    
    return output_grid
```
