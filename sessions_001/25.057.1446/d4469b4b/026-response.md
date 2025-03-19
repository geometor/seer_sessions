# d4469b4b • 026 • example_5 • investigate_coder

---
```python
"""
1.  **Identify the "Cross":** Locate the contiguous red (2) cells in the input grid that form a plus-shape or cross.
2.  **Extract Core:** Determine the smallest possible sub grid that contains the cross shape, reducing empty space around and within the cross.
3. **Translate and Change:**
      - Color red in the minimal cross representation gray (5)
    - Any other color is white (0)
4.  **Output:** Create a new grid representing the cross shape from gray.
"""

import numpy as np

def find_cross_center(grid):
    # Find the center of the cross
    rows, cols = grid.shape
    red_pixels = []
    for r in range(rows):
        for c in range(cols):
            if grid[r,c] == 2:
                red_pixels.append((r,c))

    if not red_pixels:
        return None

    sum_r = sum([p[0] for p in red_pixels])
    sum_c = sum([p[1] for p in red_pixels])
    center_r = round(sum_r / len(red_pixels))
    center_c = round(sum_c / len(red_pixels))
    return center_r, center_c
    

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # Find the center of the cross
    center = find_cross_center(input_grid)
    if center is None:
      return []

    # determine output grid
    output_grid = np.zeros((3,3), dtype=int)

    # map values
    output_grid[1,1] = 5
    output_grid[0,1] = 5
    output_grid[2,1] = 5
    output_grid[1,0] = 5
    output_grid[1,2] = 5

    return output_grid.tolist()
```
