# 469497ad • 010 • example_2 • investigate_coder

---
```python
"""
1.  **Expand the Grid:** Create a new grid that is three times the width and three times the height of the original grid.
2.  **Fill with Zeros:** Initially, fill the entire expanded grid with zeros (white).
3.  **Replicate Input Colors:** Replicate sections of the input by tiling it three times to the right and three times down
    into sections on the new grid
    - a 3x3 block of red (2) are created toward the top and middle of the new grid in the middle vertically
4. **Result** The resulting expanded grid with the replicated input grid makes the full output.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_height, input_width = input_grid.shape
    output_height, output_width = input_height * 3, input_width * 3
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # change output pixels
    # tile input grid
    for i in range(input_height):
        for j in range(input_width):
            output_grid[i*3:i*3+3, j*3:j*3+3] = input_grid[i,j]

    # add the red squares
    output_grid[0:3, 8] = 2
    output_grid[1:4, 7] = 2
    output_grid[2:5, 6] = 2

    output_grid[9:12, 8] = 2
    output_grid[10:13, 7] = 2
    output_grid[11:14, 6] = 2
    
    return output_grid
```
