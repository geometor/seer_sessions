# 5521c0d9 • 018 • refine_coder

---
```python
"""
Identify and shift colored objects (blue, yellow, and red) upwards by specific amounts,
while respecting grid boundaries and preserving the position of other colored pixels.
- Blue (color 1) objects shift up by 4 rows.
- Yellow (color 4) objects shift up by 2 rows.
- Red (color 2) objects shift up by 1 row.
"""

import numpy as np

def find_colored_objects(grid, color):
    """Finds the coordinates of all pixels of a specified color."""
    return np.argwhere(grid == color)

def shift_object_up(grid, coords, shift_amount):
    """Shifts a set of coordinates upwards by a specified amount, respecting grid boundaries."""
    new_grid = np.copy(grid)

    # Remove original object
    for r, c in coords:
        new_grid[r, c] = 0

    # Add object back at shifted position, checking boundaries
    for r, c in coords:
        new_r = max(0, r - shift_amount)  # Ensure new row is within bounds (>=0)
        new_grid[new_r, c] = grid[r,c]

    return new_grid

def transform(input_grid):
    """Transforms the input grid by shifting colored objects upwards."""
    output_grid = np.copy(input_grid)

    # Shift blue objects (color 1) up by 4
    blue_coords = find_colored_objects(output_grid, 1)
    if len(blue_coords) > 0:
        output_grid = shift_object_up(output_grid, blue_coords, 4)

    # Shift yellow objects (color 4) up by 2
    yellow_coords = find_colored_objects(output_grid, 4)
    if len(yellow_coords) > 0:
        output_grid = shift_object_up(output_grid, yellow_coords, 2)

    # Shift red objects (color 2) up by 1
    red_coords = find_colored_objects(output_grid, 2)
    if len(red_coords) > 0:
        output_grid = shift_object_up(output_grid, red_coords, 1)
        
    return output_grid
```
