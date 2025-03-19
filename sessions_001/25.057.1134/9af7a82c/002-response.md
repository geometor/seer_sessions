# 9af7a82c • 002 • example_1 • investigate_coder

---
```python
"""
The transformation takes columns of colors, sorts those columns, stacks the identified colors vertically, and fills the remaining spaces with white.
"""

import numpy as np

def get_columns(grid):
    """
    splits a grid into columns
    """
    columns = []
    for i in range(grid.shape[1]):
        columns.append(grid[:,i])
    return columns

def sort_columns_by_first_element(columns):
    """
    sorts columns from a grid by their values top down
    """
    return sorted(columns, key=lambda col: col[0] if col[0] in [1,2,3] else 999 )

def transform(input_grid):
    """
    Transforms the input grid according to the described rules.
    """
    # Get columns from the input grid.
    columns = get_columns(np.array(input_grid))

    # Sort those columns by their first element (top-down sorting)
    sorted_columns = sort_columns_by_first_element(columns)
    
    # Initialize the output grid with zeros (white).
    output_grid = np.zeros((5, 3), dtype=int)

    # Stack colors vertically and fill.
    for j, col in enumerate(sorted_columns):
        # filter out colors that are not 1 2 or 3
        valid_colors = [c for c in col if c in [1, 2, 3]]

        for i, color in enumerate(valid_colors):
            if i < 5:
                output_grid[i, j] = color

    return output_grid.tolist()
```
