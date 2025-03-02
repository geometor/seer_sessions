# ff28f65a • 016 • example_3 • investigate_coder

---
```python
"""
1.  **Identify Red Regions:** Locate all 2x2 contiguous blocks of red (value 2) pixels within the 7x7 input grid.
2.  **Center Extraction:** Focus on the central 3x3 region of the input grid. Imagine dividing the input grid in nine 3x3 segments (overlapping is allowed).
3. **Abstract Representation:** Create a 3x3 output grid.
4.  **Presence Check:** For each cell in the 3x3 output, if any of the 2x2 red squares from the input *overlap with corresponding 3x3 segment* in the original image, set that output cell to blue (1). Otherwise, set it to white (0).
"""

import numpy as np

def find_squares(grid, size, color):
    squares = []
    for i in range(grid.shape[0] - size + 1):
        for j in range(grid.shape[1] - size + 1):
            if np.all(grid[i:i+size, j:j+size] == color):
                squares.append((i, j))
    return squares

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((3, 3), dtype=int)
    
    # Find 2x2 red squares
    red_squares = find_squares(input_grid, 2, 2)

    # Check for overlap and set output grid
    for r_sq in red_squares:
        # Map the top-left corner coordinates of the 2x2 square to the output grid coordinates.
        row_out = r_sq[0] // 2  # scale the row index
        col_out = r_sq[1] // 2  # scale the col index

        # Ensure the output grid coordinate is valid
        if 0 <= row_out < 3 and 0 <= col_out < 3:
           output_grid[row_out, col_out] = 1  # change to 1 (blue)

    return output_grid
```
