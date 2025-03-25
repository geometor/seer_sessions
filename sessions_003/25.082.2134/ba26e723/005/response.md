```python
"""
1.  Iterate through each row of the input grid.
2.  For each row:
    *   If the row contains *only* yellow pixels: Change the color of yellow pixels at even column indices, *starting with index 0*, to magenta (6).
    *   If the row contains a *mixture* of colors (not only yellows): Change the yellow pixels to magenta (6) at even indices, *starting with index 0*.
3.  Output the transformed grid.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each row
    for r in range(rows):
        # Check if the row is all yellow
        row_values = [input_grid[r,c] for c in range(cols)]
        all_yellow = all(x == 4 for x in row_values)

        # Iterate through columns in the row
        for c in range(cols):
            if input_grid[r, c] == 4: #if yellow
                if c % 2 == 0: #if even index, including 0
                    output_grid[r, c] = 6  # Change to magenta

    return output_grid.tolist()
```