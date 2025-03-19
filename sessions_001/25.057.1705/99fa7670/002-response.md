# 99fa7670 • 002 • example_1 • investigate_coder

---
```python
"""
Identify non-white pixels in the input grid. For each non-white pixel, expand horizontally to the right and vertically downwards, changing white pixels to the color of the non-white pixel. Stop expansion when encountering another non-white pixel or the grid edge.
"""

import numpy as np

def transform(input_grid):
    output_grid = np.copy(input_grid)
    rows = len(input_grid)
    cols = len(input_grid[0])

    for r in range(rows):
        for c in range(cols):
            if input_grid[r][c] != 0:
                # Expand Horizontally
                for c2 in range(c + 1, cols):
                    if output_grid[r][c2] == 0:
                        output_grid[r][c2] = input_grid[r][c]
                    else:
                        break  # Stop at another non-white pixel

                # Expand Vertically
                for r2 in range(r + 1, rows):
                    if output_grid[r2][c] == 0:
                        output_grid[r2][c] = input_grid[r][c]

                        # expand the vertial line to match the horizontal line
                        for c2 in range(c + 1, cols):
                          if output_grid[r][c2] == input_grid[r][c]:
                            if output_grid[r2][c2] == 0:
                              output_grid[r2][c2] = input_grid[r][c]
                            else:
                              break # stop at another non-white pixel
                    else:
                        break  # Stop at another non-white pixel

    return output_grid
```
