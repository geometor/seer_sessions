```python
"""
Transforms an input grid by copying '5's and generating a checkerboard pattern of '1's and '5's around them. The checkerboard pattern is determined by neighboring '5's, alternating between '1' and '5'. Areas not influenced by a '5' remain '0'.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on the location of '5's and a checkerboard pattern.
    """
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Copy '5's
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 5:
                output_grid[r, c] = 5

    # Build checkerboard pattern
    for r in range(rows):
        for c in range(cols):
            if input_grid[r,c] == 0:
                neighbors = []
                if r > 0:
                    neighbors.append(output_grid[r-1, c])
                if r < rows - 1:
                    neighbors.append(output_grid[r+1, c])
                if c > 0:
                    neighbors.append(output_grid[r, c-1])
                if c < cols - 1:
                    neighbors.append(output_grid[r, c+1])
                
                if 5 in neighbors:
                    if sum(neighbors) % 10 == 5: # if only one neighbor is 5
                      output_grid[r,c] = 1
                    else:
                        # count number of 5 and 1 to determine which to add
                        count_5 = neighbors.count(5)
                        count_1 = neighbors.count(1)
                        if count_5 > count_1:
                            output_grid[r,c] = 1
                        elif count_1 > count_5:
                            output_grid[r,c] = 5
                        elif (count_5 + count_1) > 0:
                            if neighbors[0] != 0:
                                neighbor_val = neighbors[0]
                            elif len(neighbors) > 1 and neighbors[1] != 0:
                                neighbor_val = neighbors[1]
                            elif len(neighbors) > 2 and neighbors[2] != 0:
                                 neighbor_val = neighbors[2]
                            elif len(neighbors) > 3 and neighbors[3] != 0:
                                 neighbor_val = neighbors[3]
                            else:
                                 neighbor_val = 0

                            if neighbor_val == 5:
                                output_grid[r,c] = 1
                            elif neighbor_val == 1:
                                output_grid[r,c] = 5

    return output_grid.tolist()
```