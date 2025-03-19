# f35d900a • 014 • refine_coder

---
```python
"""
1.  **Mirroring:** All blue (1) and azure (8) pixels are mirrored across the horizontal center line of the grid.

2.  **Conditional Swap:**
    *   If a blue (1) pixel is mirrored by an azure (8) pixel, their colors are swapped.
    *   If a blue (1) pixel mirrors another blue (1) pixel, their colors remain blue.
    *   If an azure (8) pixel mirrors another azure (8) pixel, their colors remain azure.

3.  **Conditional Gray Filling:**
    *   If input grid has an *odd* number of rows, the center row is filled with gray (5) *if and only if* both blue(1) and azure(8) exist anywhere in the original input grid.
    *   if the input grid has an *even* number of rows, no gray filling occurs.
4. **Apply Mirror and Swap**: All transformations are applied.
"""

import numpy as np

def mirror_position(pos, max_height):
    r, c = pos
    mirrored_r = max_height - 1 - r
    return (mirrored_r, c)

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Conditional Gray Filling (only on the center line)
    center_line = rows // 2
    has_blue = False
    has_azure = False

    for r in range(rows):
      for c in range(cols):
        if input_grid[r,c] == 1:
          has_blue = True
        if input_grid[r,c] == 8:
          has_azure = True

    if rows % 2 == 1 and has_blue and has_azure:  # Only for odd-height grids with both colors
        for c in range(cols):
            output_grid[center_line, c] = 5


    # Apply mirror transformation and conditional swapping
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 1 or input_grid[r, c] == 8:
                mirrored_r, mirrored_c = mirror_position((r, c), rows)

                # Conditional Swap and Keep
                if input_grid[r, c] == 1 and input_grid[mirrored_r, mirrored_c] == 8:
                  output_grid[mirrored_r, mirrored_c] = 1
                  output_grid[r,c] = 8

                elif input_grid[r,c] == 8 and input_grid[mirrored_r, mirrored_c] == 1:
                  output_grid[mirrored_r, mirrored_c] = 8
                  output_grid[r,c] = 1
                
                # this case is already handled by copy
                #elif input_grid[r,c] == 1 and input_grid[mirrored_r, mirrored_c] == 1:
                #  output_grid[mirrored_r, mirrored_c] = 1

                #elif input_grid[r,c] == 8 and input_grid[mirrored_r, mirrored_c] == 8:
                #  output_grid[mirrored_r, mirrored_c] = 8

    return output_grid
```
