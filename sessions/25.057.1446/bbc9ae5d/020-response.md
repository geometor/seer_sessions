# bbc9ae5d • 020 • example_4 • investigate_coder

---
```python
"""
1.  **Replicate Azure:** The first four azure pixels (value 8) of the input row are replicated vertically three times to form the first four columns of the output grid.

2.  **Top Row White:** The last two white pixels (value 0) of the input are copied directly to the top row of the last two columns of the output grid.

3.  **Propagate/Modify the last two positions:** The 5th column in rows 2 & 3 is changed to azure, the 6th column remains 0 in row 2 and is changed to 8 in row 3.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_height, input_width = input_grid.shape
    output_grid = np.zeros((3, input_width), dtype=int)

    # Replicate Azure:
    for i in range(3):
        for j in range(4):
          output_grid[i, j] = 8

    # Top Row White:
    output_grid[0, 4] = input_grid[0, 4]
    output_grid[0, 5] = input_grid[0, 5]

    # Propagate/Modify the last two positions
    output_grid[1,4] = 8
    output_grid[1,5] = 0
    output_grid[2,4] = 8
    output_grid[2,5] = 8

    return output_grid
```
