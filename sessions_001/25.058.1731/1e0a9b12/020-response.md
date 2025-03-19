# 1e0a9b12 • 020 • refine_coder

---
```python
"""
1.  **Blue Pixel Shift:** If a blue pixel is located in the 4th column (index 3) and its row index is 2 or greater, move it down by one row.
2.  **Green Pixel Shift:** Identify green pixels. if green pixel is in the second column (index 1) and its row index is greater or equal to 1, move it down by one row.
3.  **Magenta Pixel Shift:** If there is a magenta pixel at position [3, 0], move it down by one row.
4.  **Red Pixel Shift**: If a red pixel is located in the 5th column (index 4) and its row index is less than 2, move it down and one position to the left, by one row.
5.  **Copy Remaining:** Any other non-zero pixel that is not affected by the above rules should remain in its original position in the output grid.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each pixel of the input grid
    for r in range(rows):
        for c in range(cols):
            # Blue Pixel Shift
            if input_grid[r, c] == 1 and c == 3 and r >= 2:
                output_grid[r + 1, c] = 1
            # Green Pixel Shift
            elif input_grid[r,c] == 3 and c == 1 and r >= 1:
                output_grid[r+1,c] = 3
            # Magenta Pixel Shift
            elif input_grid[r, c] == 6 and r == 3 and c == 0:
                output_grid[r + 1, c] = 6
            # Red pixel Shift
            elif input_grid[r,c] == 2 and c == 4 and r < 2:
                output_grid[r+1,c-1] = 2
            # Copy Remaining
            elif input_grid[r, c] != 0:
                output_grid[r, c] = input_grid[r, c]

    return output_grid
```
