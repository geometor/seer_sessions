```python
"""
1.  **Identify Gray Pixels:** Locate all pixels in the input grid that have the value 5 (gray).

2.  **Conditional Replacement:** For each gray pixel:
    *   If the gray pixel is in the top row change it to zero.
    *   Check the pixels directly to the *left* and *right* of the current gray pixel.
        *   If a neighbor exists and *is not* gray (and not 0), replace gray by that neighbor's value in the output grid.
        *   If both neighbors exist, and meet the conditions, prioritize change to the left pixel color.

3.  **Preserve Unchanged Pixels:** All other pixels that are not gray, or gray pixels with no non-gray/non-zero neighbors to the left or right, should remain unchanged in the output grid.

4. If there is no non-gray and non-zero neighbor on either side,
 - if the gray is to the left of a non-gray, non-zero color - change the gray to zero
 - otherwise,
    - If the row of the gray contains a non-zero, non-gray color on the left of gray, change gray to the color furthest to the left.
    - if none of the above, change gray to zero
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # iterate through each cell in the grid
    for r in range(rows):
        for c in range(cols):
            # Identify Gray Pixels
            if input_grid[r, c] == 5:
                # Conditional Replacement
                # if the pixel is gray, and top row, make output 0
                if r == 0:
                    output_grid[r,c] = 0
                    continue
                
                left_neighbor = c - 1
                right_neighbor = c + 1
                left_val = input_grid[r, left_neighbor] if left_neighbor >= 0 else None
                right_val = input_grid[r, right_neighbor] if right_neighbor < cols else None
                
                # Check neighbors
                if left_val is not None and left_val != 5 and left_val != 0:
                    output_grid[r, c] = left_val
                elif right_val is not None and right_val != 5 and right_val != 0:
                    output_grid[r, c] = right_val
                # now the complicated "if none of the above" conditions
                else:
                    # find leftmost non-gray, non-zero
                    leftmost_val = 0
                    
                    for i in range(c):
                        if input_grid[r,i] != 5 and input_grid[r,i] !=0:
                            leftmost_val = input_grid[r,i]
                    output_grid[r,c] = leftmost_val


    return output_grid
```