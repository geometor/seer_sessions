```python
"""
The transformation rule involves a prioritized horizontal fill from the top-right element combined with a downward expansion of colors for any non-zero colored cells.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Horizontal Fill (Top Right)
    top_right_color = input_grid[0, cols - 1]
    if top_right_color != 0:
        for r in range(1,rows):
            for c in range(0, cols):
                output_grid[r,c] = top_right_color

    # Vertical Fill
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] != 0 and not (r == 0 and c == cols -1 and top_right_color!=0):
                for r_below in range(r + 1, rows):
                    output_grid[r_below, c] = input_grid[r, c]
    
    # Apply horizontal fill after.
    if top_right_color != 0:
        for r in range(1,rows):
           output_grid[r,:] = top_right_color

    return output_grid
```
