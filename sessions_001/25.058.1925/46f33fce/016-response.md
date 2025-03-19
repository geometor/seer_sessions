# 46f33fce • 016 • example_3 • investigate_coder

---
```python
"""
Transforms the input grid by expanding regions of non-zero colored pixels
outwards until they encounter other colored regions or the grid boundaries.
Each color expands into a rectangular area that takes 1/4th total input area.
"""

import numpy as np

def get_object_locations(grid):
    """Finds the locations of all non-zero pixels in the grid."""
    locations = {}
    for r, row in enumerate(grid):
        for c, value in enumerate(row):
            if value != 0:
                if value not in locations:
                    locations[value] = []
                locations[value].append((r, c))
    return locations

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # get locations of non-zero pixels
    object_locations = get_object_locations(input_grid)

    # target expansion area
    target_height = rows // 2
    target_width = cols // 2

    # expand each color region
    for color, locations in object_locations.items():
        # Assuming only one object per color for now, take first location
        start_row, start_col = locations[0]

        # calculate boundaries
        min_row = max(0, start_row - target_height + 1)
        max_row = min(rows, start_row + target_height)  # Exclusive bound
        min_col = max(0, start_col - target_width + 1)
        max_col = min(cols, start_col + target_width)  # Exclusive bound

        # change output pixels in expanded area
        for r in range(min_row, max_row):
            for c in range(min_col, max_col):
                output_grid[r, c] = color

    return output_grid
```
