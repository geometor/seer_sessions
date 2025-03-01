# f2829549 • 029 • refine_coder

---
```python
"""
The transformation rule involves analyzing each column of the input grid. If a column has a predominant color (appearing more times than any other color) and the column contains at least one other different color, the corresponding column in the output grid is filled with green (3). If a column has a single, unique color, or a predominant color, but no other numbers, then output the original column.
"""

import numpy as np

def check_predominant_color_with_others(column):
    """
    Checks if a column has a predominant color and if the column also has at least one other color.
    Returns the predominant color if the conditions are met, otherwise returns None.
    """
    counts = {}
    for x in column:
        counts[x] = counts.get(x, 0) + 1
    
    predominant_color = None
    predominant_count = 0
    for color, count in counts.items():
        if count > predominant_count:
            predominant_count = count
            predominant_color = color
    
    if predominant_color is not None and len(counts) > 1:
        return predominant_color
    else:
        return None

def transform(input_grid):
    """
    Transforms the input grid according to the specified rules.
    """
    input_grid = np.array(input_grid)
    rows = input_grid.shape[0]
    cols = input_grid.shape[1]
    output_grid = np.array(input_grid).copy() # initialize to original

    for j in range(cols):
        column = input_grid[:, j]
        predominant_color = check_predominant_color_with_others(column)

        if predominant_color is not None:
            output_grid[:, j] = 3  # set the output column to green
    
    return output_grid.tolist()
```
