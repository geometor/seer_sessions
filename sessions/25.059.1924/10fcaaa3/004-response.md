# 10fcaaa3 • 004 • example_1 • investigate_coder

---
```python
"""
1.  **Expand Input Grid:** The input grid is expanded to double its height and double *plus* double its width.
2. **Fill New Rows with background and secondary color:** all odd rows, starting at 1, is filled with `8`. Each element at an odd index is `8`.
3.  **Replicate Original Cells:** The original cells from the input grid are replicated in the output grid.
    *   Each original cell is copied into the output grid multiple times.
    *   The original cell located at (r, c) in the input appears at positions (2r, 2c) and (2r, 2c + 4) in the output.
4.  **Maintain Other cells:** Any empty cell `0` is maintained in the output at position (2r, 2c)
.

Essentially the output is structured as such:
- original input copied to maintain relative positions
- original input copied and x position + 4 added
- odd rows are filled with an alternating pattern

Example

```
0 5 0 0     ->   8 0 8 0 8 0 8 0
                   0 5 0 0 0 5 0 0
                   8 0 8 0 8 0 8 0
                   0 5 0 0 0 5 0 0
```
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_height, input_width = input_grid.shape
    output_height = input_height * 2
    output_width = input_width * 4
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Fill odd rows
    for i in range(output_height):
        if (i+1) % 2 != 0:
          for j in range(output_width):
              if (j+1) % 2 != 0:
                output_grid[i,j] = 8

    # replicate original cells
    for row in range(input_height):
        for col in range(input_width):
            output_grid[2*row, 2*col] = input_grid[row,col]
            output_grid[2*row, 2*col + 4] = input_grid[row, col]

    return output_grid
```
