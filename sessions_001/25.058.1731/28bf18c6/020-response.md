# 28bf18c6 • 020 • refine_coder

---
```python
"""
1.  **Identify Unique Colors:** Find all unique colors present in the input grid.
2.  **Find Bottom-Right Pixel:** For *each* unique color, find the pixel of that color that is furthest to the bottom-right.  This is done by scanning rows from bottom to top, and within each row, from right to left.
3. **Stack Pixels** Create a new output grid. For each unique bottom-right pixel found in step 2 create a new row in the output grid. The row will contain a single pixel of the same color. The order of the colors in the output grid is maintained from step 2.
"""

import numpy as np

def find_bottom_right_pixel(grid, color):
    # Iterate from bottom-right to top-left
    for r in range(grid.shape[0] - 1, -1, -1):
        for c in range(grid.shape[1] - 1, -1, -1):
            if grid[r, c] == color:
                return (r, c)
    return None  # Should not happen if color is present

def transform(input_grid):
    # Convert input_grid to a NumPy array
    input_grid = np.array(input_grid)

    # 1. Identify Unique Colors
    unique_colors = np.unique(input_grid)
    unique_colors = unique_colors[unique_colors != 0] # remove background color

    # 2. Find Bottom-Right Pixel for each color
    bottom_right_pixels = []
    for color in unique_colors:
        pixel_coords = find_bottom_right_pixel(input_grid, color)
        if pixel_coords:  # Ensure a pixel was found
            bottom_right_pixels.append((color, pixel_coords))

    # 3. Stack Pixels in output grid
    output_grid = np.zeros((len(bottom_right_pixels), 1), dtype=int)
    for i, (color, _) in enumerate(bottom_right_pixels):
        output_grid[i, 0] = color

    return output_grid.tolist()
```
