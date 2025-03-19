# 49d1d64f • 008 • example_2 • investigate_coder

---
```python
"""
The input grid is expanded to create the output grid. The transformation involves a combination of mirroring and padding. The input grid is horizontally mirrored, with the central column preserved.  Then, it is vertically mirrored with an overlap. Finally, zeros (white) are added to the corners of the output grid.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_height = len(input_grid)
    input_width = len(input_grid[0])
    output_height = 2 * input_height
    output_width = 2 * input_width - 1
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # copy rows of input to output, horizontal mirroring
    for row in range(input_height):
        for col in range(input_width):
            output_grid[row][col] = input_grid[row][col]
            output_grid[row][output_width - 1 - col] = input_grid[row][col]

    # duplicate rows, vertical mirroring
    for row in range(input_height):
       output_grid[output_height-1-row] = output_grid[row]

    # pad with zeros is not necessary, as np.zeros was used

    return output_grid
```
