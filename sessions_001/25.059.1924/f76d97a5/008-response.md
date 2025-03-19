# f76d97a5 • 008 • refine_coder

---
```python
"""
1.  **Identify Original Yellow:** Locate all pixels that are initially yellow (color 4) in the input grid.
2.  **Conditional Gray Conversion:**
    *   **If** there are gray (color 5) pixels in the input grid, change *all* of them to yellow (color 4).
3.  **Conditional Yellow Conversion:**
    *   **If** there were any pixels that were *originally* yellow (identified in step 1), change *all* of them to white (color 0).
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    
    # Identify Original Yellow
    initial_yellow_pixels = []
    for i in range(input_grid.shape[0]):
        for j in range(input_grid.shape[1]):
          if input_grid[i,j] == 4:
            initial_yellow_pixels.append((i,j))

    # Conditional Gray Conversion
    gray_exists = False
    for i in range(input_grid.shape[0]):
        for j in range(input_grid.shape[1]):
            if input_grid[i,j] == 5:
                gray_exists = True
                break
        if gray_exists:
            break

    if gray_exists:
      for i in range(input_grid.shape[0]):
        for j in range(input_grid.shape[1]):
          if output_grid[i,j] == 5:
            output_grid[i,j] = 4

    # Conditional Yellow Conversion
    if len(initial_yellow_pixels) > 0:
        for (i,j) in initial_yellow_pixels:
            output_grid[i,j] = 0


    return output_grid
```
