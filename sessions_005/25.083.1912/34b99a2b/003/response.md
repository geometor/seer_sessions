```python
"""
1.  **Output Grid Size:** The output grid always has 4 columns, and the same number of rows as the input grid.
2.  **Yellow Anchor:** In each input row, there's always a yellow (4) pixel in the 5th column (index 4).  This seems to serve as an anchor point.
3.  **Input Transformation to Output**: Extract 2 x 2 subgrids from the input, using the coordinates of the yellow pixels in each row as the lower-right corner of the subgrid. Rotate each extracted subgrid by 180 degrees.
4. Place each rotated 2x2 subgrid into the output grid with the following rule:
    - Use the row index from the input.
    - The rotated subgrid will occupy column indices 0,1 and 2,3 of the output.
"""

import numpy as np

def rotate_180(subgrid):
    """Rotates a 2x2 subgrid by 180 degrees."""
    return np.rot90(subgrid, 2)

def transform(input_grid):
    # initialize output_grid
    rows = len(input_grid)
    cols = 4
    output_grid = np.zeros((rows, cols), dtype=int)

    # iterate through rows
    for r in range(rows):
        # extract 2x2 subgrid, anchor is one column left of yellow
        anchor_col = 4 -1
        subgrid = input_grid[r:r+2, anchor_col-1:anchor_col+1]

        #check if its a valid 2x2 grid
        if subgrid.shape == (2, 2):
            # rotate the subgrid
            rotated_subgrid = rotate_180(subgrid)

            # place in output grid
            output_grid[r:r+2, 0:2] = rotated_subgrid
        else:
             # handle edge case, use 1x2 grid instead, transpose
            if r+1 >= rows:
                subgrid = input_grid[r:r+1, anchor_col-1:anchor_col+1]
                rotated_subgrid = subgrid.T
                output_grid[r:r+1, 0:2] = rotated_subgrid
            # use 2x1
            elif anchor_col == 0:
                subgrid = input_grid[r:r+2, anchor_col:anchor_col+1]
                rotated_subgrid = subgrid.T
                output_grid[r:r+2, 0:1] = rotated_subgrid



    return output_grid
```