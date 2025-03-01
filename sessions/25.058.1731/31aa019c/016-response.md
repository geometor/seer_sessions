# 31aa019c • 016 • example_3 • investigate_coder

---
```python
"""
1. **Identify the Area of Interest:** Scan the input grid. The area of interest are all pixels that are non-zero and have at least one neighbor (up, down, left, right, or diagonal) that is non-zero.
2.  **Locate Subgrid:** If an area of interest is found, identify the bottom-right-most pixel, and define the 3x3 region in the output grid at that bottom right corner of the area of interest.
3. **Fill Output:** If no region is found, the output is all zeros. If it exists:
    fill the region with color '2' except for the central pixel which is '3'.
4.  **Other Pixels:** All other pixels in the output grid are set to 0.
"""

import numpy as np

def find_area_of_interest(grid):
    rows, cols = grid.shape
    area_pixels = []
    for r in range(rows):
        for c in range(cols):
            if grid[r,c] != 0:
                is_in_area = False
                for dr in [-1,0,1]:
                    for dc in [-1,0,1]:
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] != 0:
                            is_in_area = True
                            break
                    if is_in_area:
                        break
                if is_in_area:
                  area_pixels.append((r,c))
    return area_pixels

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Find the area of interest
    area_pixels = find_area_of_interest(input_grid)

    if len(area_pixels) > 0:
        #find bottom right
        max_r = -1
        max_c = -1
        for r,c in area_pixels:
            if r > max_r:
                max_r = r
                max_c = c
            elif r == max_r and c > max_c:
                max_c = c

        # fill output
        for dr in range(-1,2):
            for dc in range(-1,2):
                nr, nc = max_r + dr, max_c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    if dr == 0 and dc == 0:
                      output_grid[nr,nc] = 3
                    else:
                      output_grid[nr,nc] = 2


    return output_grid
```
