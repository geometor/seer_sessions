```python
"""
Transforms an input grid by reordering colors within each column, propagating the highest colors downwards.
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    rows = len(input_grid)
    cols = len(input_grid[0])

    # Iterate through each column
    for c in range(cols):
        #find non-zero colors present in current col, sort desc
        colors = sorted(list(set(input_grid[:,c])), reverse=True)
        colors = [color for color in colors if color!=0]

        #iterate through found colors
        row_index = 0
        for color in colors:
            #fill output with colour
            for r in range(rows):
                if input_grid[r,c] == color:
                    output_grid[row_index,c] = color
                    row_index +=1

    return output_grid
```