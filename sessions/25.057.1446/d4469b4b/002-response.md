# d4469b4b • 002 • example_1 • investigate_coder

---
```python
"""
1.  **Focus:** Consider the central 3x3 region of the input grid.
2. **Subgrids:** iterate the four 2 x 2 subgrids, starting at these corners:
   * top-left: (0,0)
   * top-right: (0,1)
   * bottom-left: (1,0)
   * bottom-right: (1,1)

3.  **Condensation Rule:**
    *   For each 2x2 subgrid in the input, check all pixels.
    *   If any pixel within the 2x2 subgrid is red (value 2), set the corresponding output pixel to gray (value 5).
    *   If all pixels within the 2x2 subgrid are white (value 0), set the corresponding output pixel to white (value 0).
4. construct a new 3 x 3 output grid of the pixels from processing the 2 x 2 subgrids.
"""

import numpy as np

def transform(input_grid):
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros((3, 3), dtype=int)

    # Iterate through the central 3x3 region of the input grid
    for i in range(rows - 2):  # corrected loop end
        for j in range(cols-2):  # corrected loop end
           # Extract the 2x2 subgrid
           subgrid = input_grid[i:i+2, j:j+2]

           # Check if any pixel in the subgrid is red (2)
           if 2 in subgrid:
              output_grid[i,j] = 5  # Set corresponding output pixel to gray (5)
           else:
              output_grid[i, j] = 0 # keep output as white
    return output_grid.tolist()
```
