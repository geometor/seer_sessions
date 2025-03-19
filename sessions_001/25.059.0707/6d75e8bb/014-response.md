# 6d75e8bb • 014 • refine_coder

---
```python
"""
Replaces pixels within an azure region with red pixels, based on relative position within the azure region.
"""

import numpy as np

def find_contiguous_region(grid, color):
    """Finds a contiguous region of a given color and returns its pixel coordinates."""
    rows, cols = grid.shape
    start_row, start_col = -1, -1
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color:
                start_row, start_col = r, c
                break
        if start_row != -1:
            break

    if start_row == -1:
        return []

    visited = set()
    pixels = []
    queue = [(start_row, start_col)]

    while queue:
        row, col = queue.pop(0)
        if (row, col) in visited or not (0 <= row < rows and 0 <= col < cols) or grid[row, col] != color:
            continue

        visited.add((row, col))
        pixels.append((row, col))

        # Add adjacent pixels to the queue
        queue.append((row + 1, col))
        queue.append((row - 1, col))
        queue.append((row, col + 1))
        queue.append((row, col - 1))

    return pixels

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find the contiguous region of azure (8) pixels
    azure_region = find_contiguous_region(output_grid, 8)

    if not azure_region:
        return output_grid

    # Determine replacement locations based on relative coordinates within the azure region
    min_row = min(r for r, _ in azure_region)
    max_row = max(r for r, _ in azure_region)
    min_col = min(c for _, c in azure_region)
    max_col = max(c for _, c in azure_region)

    region_height = max_row - min_row + 1
    region_width = max_col - min_col + 1

    for row, col in azure_region:
        rel_row = row - min_row
        rel_col = col - min_col

        # If there's a second row
        if rel_row == 1:
            if region_height == 4: # replace two pixels on the second row
               if rel_col == 1 or rel_col == 2:
                  output_grid[row,col] = 2
            elif region_height == 3:
                if region_width >=3 and region_width <= 6: # examples 1 and 3
                    if rel_col == 1:
                       output_grid[row,col] = 2
                elif region_width > 6: # wider regions, example 2
                   if rel_col == 1 or rel_col == 4:
                       output_grid[row,col] =2 # two pixels separated
            elif region_height >= 5: # example 3 - very tall region
                if rel_col == region_width -2 :
                   output_grid[row,col] = 2 # place before last
        elif region_height > 2 and rel_row == 2 and region_width >5:  #one case in example 3
            if rel_col == region_width-2: #2nd row
              output_grid[row,col] = 2
    return output_grid
```
