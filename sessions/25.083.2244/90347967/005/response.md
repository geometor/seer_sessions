```python
"""
Non-zero pixels are treated as objects. These objects are reordered
vertically, with their output order being the reverse of their input
vertical order.  Objects maintain their original column if possible. All objects
are shifted upwards to occupy the highest possible rows.
"""

import numpy as np

def get_non_zero_objects(grid):
    # get a list of (row, col, value) tuples for non-zero elements
    objects = []
    for r, row in enumerate(grid):
        for c, value in enumerate(row):
            if value != 0:
                objects.append((r, c, value))
    return objects

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # identify non-zero pixels and their coordinates
    objects = get_non_zero_objects(input_grid)

    # sort the objects by their row index (vertical order)
    sorted_objects = sorted(objects, key=lambda x: x[0])

    # reverse the vertical order
    reversed_objects = sorted_objects[::-1]

    # construct the output grid
    output_row = 0
    output_col_counts = [0] * cols #keep track of how many have been placed in each col

    for obj in reversed_objects:
        _, original_col, value = obj
        output_grid[output_row, original_col] = value
        output_col_counts[original_col] +=1
        output_row = 0
        for c in range(cols):
          output_row = max(output_row, output_col_counts[c])

    return output_grid.tolist()
```