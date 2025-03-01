# 746b3537 • 012 • refine_coder

---
```python
"""
Identify rows containing at least one blue or red object. Extract these rows
into the output grid, preserving their original order. If no blue or red
objects are found, output is an empty grid of 1xN where N matches the number of
columns in the input grid.
"""

import numpy as np

def find_objects(row):
    """
    Finds objects (contiguous blocks of the same color) within a row.
    Returns a list of tuples, where each tuple contains (color, start_index, end_index).
    """
    objects = []
    if len(row) == 0:
        return objects

    current_color = row[0]
    start_index = 0
    for i in range(1, len(row)):
        if row[i] != current_color:
            objects.append((current_color, start_index, i - 1))
            current_color = row[i]
            start_index = i
    objects.append((current_color, start_index, len(row) - 1))
    return objects

def has_blue_or_red_object(row):
    """
    Checks if a row contains at least one blue (1) or red (2) object.
    """
    objects = find_objects(row)
    for color, _, _ in objects:
        if color == 1 or color == 2:
            return True
    return False
    
def is_solid_color(row):
    """
    Checks if row is a single solid color
    """
    objects = find_objects(row)
    return len(objects) == 1

def transform(input_grid):
    # Get the dimensions of the input grid.
    rows, cols = input_grid.shape

    # Initialize an empty list to hold the rows to be extracted.
    output_rows = []

    # Iterate through each row of the input grid.
    for i in range(rows):
        row = input_grid[i, :]
        # Check if a row contains any objects of interest
        if not is_solid_color(row) and has_blue_or_red_object(row):
            output_rows.append(row)

    # If no blue or red objects are found, return a 1xcol empty grid.
    if not output_rows:
        return np.zeros((1, cols), dtype=int)

    # Convert the list of rows to a NumPy array.
    output_grid = np.array(output_rows)

    return output_grid
```
