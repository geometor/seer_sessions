# db3e9e38 • 002 • example_1 • investigate_coder

---
```python
"""
1.  **Identify the vertical line:** Find the contiguous vertical line of orange (7) pixels. Note its vertical extent and horizontal position.
2.  **Construct the vertical arm:** Maintain the original orange (7) line in the output grid.
3.  **Construct the horizontal arms:** For each row containing part of the original vertical orange line, place an azure (8) pixel to the immediate left and right of the orange pixel.
4. **extend horizontal arms:** Extend the arm to the border, alternating the colors of the pixels
5.  **Preserve the background:** All other pixels in the input grid that are not part of the constructed cross should retain their original values in the output grid.
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
        # Construct the horizontal arms
        for row_index in range(start_row, end_row + 1):
            # output_grid[row_index, col_index] = 7 # this is redundant
            # fill left
            color = 8
            for c in range(col_index -1, -1, -1):
                output_grid[row_index, c] = color
                color = 7 if color == 8 else 8
            # fill right
            color = 8
            for c in range(col_index + 1, cols):
                output_grid[row_index, c] = color
                color = 7 if color == 8 else 8
    
    return output_grid
```
