# d9f24cd1 • 006 • example_1 • investigate_coder

---
```python
"""
1.  **Copy the grid:** Start with a copy of the input grid.
2.  **Preserve gray pixels** Keep existing gray (5) pixels in their original positions.
3. **Fill red columns:** In the output grid, make every other columns that have red pixels, to only contain red pixels.
4. **Propagate to gray Columns:** Take every gray (5) pixel. If there is space on either side of it, Fill the whole column with 2 (red).
5. If a column has both red and gray, fill every empty (0) cell to the left of the gray with red.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find columns with red pixels
    red_cols = []
    for c in range(cols):
        for r in range(rows):
            if output_grid[r,c] == 2:
                red_cols.append(c)
                break;

    # Fill those columns with red
    for c in red_cols:
        for r in range(rows):
            output_grid[r, c] = 2

    # Iterate through gray pixels
    for r in range(rows):
        for c in range(cols):
            if output_grid[r, c] == 5:
                # Fill current column with red up to the gray pixel
                for r_above in range(r):
                  output_grid[r_above,c] = 2
                
                #Fill to left with red.
                for c_left in range(c):
                    output_grid[r,c_left] = 2
                
                # Check left and right and fill the columns
                if c > 0:
                    for r_index in range(rows):
                        output_grid[r_index,c-1] = 2

                if c < cols-1:
                    for r_index in range(rows):
                        output_grid[r_index, c+1] = 2


    return output_grid
```
