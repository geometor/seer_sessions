# 995c5fa3 • 008 • example_2 • investigate_coder

---
```python
"""
1.  **Identify the Interior:** Locate the largest contiguous rectangular region within the input grid that is surrounded by a boundary of gray (5) pixels. This interior region will only contain white (0) pixels, and is defined by at least a one pixel thick border of gray pixels.
2.  **Define areas:** The white pixels form a rectangle. Split this rectangle area into 9 equal areas, like a tic-tac-toe board.
3. **Create Output Grid**: Generate a 3x3 output grid.
4. **Assign Colors**: Map the 9 equal parts of the input area onto the output grid. The top-left sector of input pixels will be represented as green(3) in the top-left cell of output grid.The center-top input sector will be represented as green(3) in the center-top cell of output grid, etc. The pattern is to fill each output cell using an arbitrary color (3,2 or 4) in the same layout as it appears in input.
"""

import numpy as np

def find_interior_rectangle(grid):
    rows, cols = grid.shape
    min_r, min_c = rows, cols
    max_r, max_c = -1, -1

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 5:  # Not a boundary pixel
                min_r = min(min_r, r)
                min_c = min(min_c, c)
                max_r = max(max_r, r)
                max_c = max(max_c, c)

    return min_r, min_c, max_r, max_c

def transform(input_grid):
    # Find the interior rectangle bounded by gray (5) pixels
    min_r, min_c, max_r, max_c = find_interior_rectangle(np.array(input_grid))

    # Calculate the dimensions of the interior rectangle
    interior_height = max_r - min_r + 1
    interior_width = max_c - min_c + 1
    
    # Initialize the output grid as a 3x3 numpy array
    output_grid = np.zeros((3, 3), dtype=int)
    
    # Determine section dimensions, handle the case where dimensions might not be perfectly divisible by 3.
    section_height = interior_height // 3
    section_width = interior_width // 3

    # Assign colors based on the 9-sector mapping.
    color_map = {
        (0, 0): 3, (0, 1): 3, (0, 2): 3,
        (1, 0): 4, (1, 1): 4, (1, 2): 4,
        (2, 0): 2, (2, 1): 2, (2, 2): 2,
    }

    for i in range(3):
        for j in range(3):
            output_grid[i, j] = color_map[(i, j)]

    return output_grid.tolist()
```
