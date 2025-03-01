# 6d75e8bb • 020 • refine_coder

---
```python
"""
Identify contiguous azure regions. Within each region, identify "indentations" or "protrusions".
An indentation or protrusion can be defined based on a change in the width.
Change the color of the azure pixels within these indentations/protrusions to red, starting from
the point where the width changes, and filling inwards or outwards as appropriate to create a contiguous red section.
The overall effect is to "smooth out" or "fill in" parts of the azure shape.
"""

import numpy as np

def get_object_coords(grid, color):
    """Returns a list of (row, col) coordinates for the given color."""
    return list(zip(*np.where(grid == color)))

def get_adjacent_coords(grid, coord):
    r, c = coord
    rows, cols = grid.shape
    adjacent = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            adjacent.append((nr, nc))
    return adjacent

def find_indentations_protrusions(grid, azure_coords):
    """
    Identifies indentations and protrusions within azure regions.
    Returns a list of coordinates to be recolored.
    """
    coords_to_recolor = []
    # Analyze rows
    for r in range(grid.shape[0]):
        azure_in_row = [c for (row, c) in azure_coords if row == r]
        azure_in_row.sort()
        if len(azure_in_row) > 1:
            for i in range(1, len(azure_in_row)):
                if azure_in_row[i] - azure_in_row[i-1] > 1: #indentation on row
                   coords_to_recolor.extend([(r,c) for c in range(azure_in_row[i-1] + 1, azure_in_row[i])])

    # Analyze columns
    for c in range(grid.shape[1]):
        azure_in_col = [r for (r, col) in azure_coords if col == c]
        azure_in_col.sort()
        if len(azure_in_col) > 1:
            for i in range(1, len(azure_in_col)):
                if azure_in_col[i] - azure_in_col[i-1] > 1: #indentation on col
                   coords_to_recolor.extend([(r,c) for r in range(azure_in_col[i-1] + 1, azure_in_col[i])])

    return coords_to_recolor

def transform(input_grid):
    # Initialize output_grid as a copy of the input.
    output_grid = np.copy(input_grid)

    # Find all azure regions.
    azure_coords = get_object_coords(input_grid, 8)

    # Find indentations and protrusions within each azure region.
    coords_to_recolor = find_indentations_protrusions(input_grid, azure_coords)

    # Recolor the identified pixels to red.
    for r, c in coords_to_recolor:
        if (r,c) in azure_coords:
          output_grid[r, c] = 2  # Red

    return output_grid
```
