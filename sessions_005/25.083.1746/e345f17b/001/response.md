```python
"""
1.  **Observe:** Examine the input grid and identify regions of magenta (6) and gray (5).
2.  **Analyze:** For each cell identify a 2x2 region moving left to right top to bottom.
3.  **Transform** Count the magenta pixels in the 2x2, if there are any, place a single yellow in a corresponding location of the 4x4 output grid.
4.  **Condense and Output:** create the 4 x 4 grid, filling the output positions with a yellow (4) for locations that had magenta (6) and fill all other values with white (0).
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((4, 4), dtype=int)
    input_height = len(input_grid)
    input_width = len(input_grid[0])
    
    # iterate over possible 2x2 regions in the input
    for row in range(min(input_height-1,4)):
      for col in range(min(input_width-1,4)):
        # check the 2x2
        magenta_count = 0
        for i in range(2):
            for j in range(2):
                if row+i < input_height and col +j < input_width:
                    if input_grid[row + i][col + j] == 6:
                        magenta_count +=1

        # output a yellow if magenta exists
        if magenta_count > 0:
            output_grid[row][col] = 4

    return output_grid
```