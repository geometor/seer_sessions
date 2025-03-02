# 75b8110e • 032 • refine_coder

---
```python
"""
1.  **Identify Key Colors:** The colors involved in the transformation are 0 (white), 4 (yellow), and 5 (gray).
2.  **2x2 Window Scan:** Iterate through the input grid using a 2x2 window, moving one pixel at a time (without overlap in the iteration, but the windows themselves overlap because we move one pixel at a time).
3.  **Intersection Check:** For each 2x2 window, check if it contains at least two of the key colors (0, 4, and 5).
4.  **Output Pixel Placement:** If an "intersection" (at least two key colors present) is found in the 2x2 window:
    *   The output grid's dimensions are determined by dividing the input grid's dimensions by 2 (integer division, rounding down). For example input 8x8 becomes 4x4, 6x15 is 3x7, 4x6 is 2x3.
    *   Place a pixel in the output grid at the corresponding location. The row and column indices of the output pixel are the row and column indices of the *top-left* pixel of the 2x2 window, each divided by 2 (integer division).
    *   The color of the output pixel is the color of the *top-left* pixel of the 2x2 window in the input grid.
5. **Complete Output:** The output is built up of pixels based on these 2x2 intersection checks.
"""

import numpy as np

def check_intersection_2x2(grid, r, c, colors):
    """
    Checks for an intersection of at least 2 different colors within a 2x2 window.
    """
    window_colors = set()
    for i in range(2):
        for j in range(2):
            nr, nc = r + i, c + j
            if 0 <= nr < grid.shape[0] and 0 <= nc < grid.shape[1]:
                window_colors.add(grid[nr, nc])
    return len(window_colors.intersection(colors)) >= 2

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.zeros((input_grid.shape[0] // 2, input_grid.shape[1] // 2), dtype=int)
    colors_of_interest = {0, 4, 5}

    # Iterate through the input grid using a 2x2 window
    for r in range(input_grid.shape[0] - 1):
        for c in range(input_grid.shape[1] - 1):
            # Check for intersection in the 2x2 window
            if check_intersection_2x2(input_grid, r, c, colors_of_interest):
                # Place pixel in output grid
                output_grid[r // 2, c // 2] = input_grid[r, c]

    return output_grid
```
