# 234bbc79 • 020 • example_4 • investigate_coder

---
```python
"""
Transforms an input grid by replacing gray (5) pixels with white (0) and some red(2) pixels to white(0).
All gray (5) pixels are changed to white (0).
Some red(2) pixels are replaced with white (0) if adjacent horizontally to gray(5)
Blue (1) pixels and any othe original pixels, including white(0) are unchanged.
"""

import numpy as np

def transform(input_grid):
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    for r in range(rows):
        for c in range(cols):
            # If the pixel is gray (5), change it to white (0)
            if input_grid[r, c] == 5:
                output_grid[r, c] = 0
            #if pixel is red (2)
            elif input_grid[r,c] == 2:
                #check left
                if c > 0 and input_grid[r,c-1] == 5:
                    output_grid[r,c] = 0
                #check right
                elif c < cols - 1 and input_grid[r, c+ 1] == 5:
                    output_grid[r,c] = 0
    return output_grid
```
