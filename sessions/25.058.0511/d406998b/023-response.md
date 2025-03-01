# d406998b • 023 • refine_coder

---
```python
"""
1. Identify Gray Rectangles: Locate rectangular regions of gray pixels in the input grid.
2. Conditional Replacement: Within those identified gray rectangles, replace a subset of the gray pixels with green pixels. The specific gray pixels replaced are determined by their relative position within the grey rectangle. Specifically, pixels that form a corner of the largest solid grey rectangle.
"""

import numpy as np

def find_largest_gray_rectangle(grid):
    """Finds the largest contiguous gray rectangle in the grid."""
    max_area = 0
    best_rect = None

    for r1 in range(grid.shape[0]):
        for c1 in range(grid.shape[1]):
            if grid[r1, c1] == 5:  # Start of a potential gray pixel
                for r2 in range(r1, grid.shape[0]):
                    for c2 in range(c1, grid.shape[1]):
                        # Check if all pixels within (r1, c1) to (r2, c2) are gray
                        is_gray_rect = True
                        for r in range(r1, r2 + 1):
                            for c in range(c1, c2 + 1):
                                if grid[r, c] != 5:
                                    is_gray_rect = False
                                    break
                            if not is_gray_rect:
                                break

                        if is_gray_rect:
                            area = (r2 - r1 + 1) * (c2 - c1 + 1)
                            if area > max_area:
                                max_area = area
                                best_rect = (r1, c1, r2, c2)

    return best_rect

def transform(input_grid):
    # Initialize output grid as a copy of the input grid
    output_grid = input_grid.copy()

    # Find the largest gray rectangle
    rect = find_largest_gray_rectangle(input_grid)

    if rect:
        r1, c1, r2, c2 = rect
        # Replace corner pixels with green
        if output_grid[r1,c1] == 5:
          output_grid[r1, c1] = 3
        if output_grid[r1,c2] == 5:
          output_grid[r1, c2] = 3
        if output_grid[r2,c1] == 5:
           output_grid[r2, c1] = 3
        if output_grid[r2,c2] == 5:
          output_grid[r2, c2] = 3


    return output_grid
```
