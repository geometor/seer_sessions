```python
"""
1.  **Identify Blue Objects:** Find all contiguous regions (objects) of blue (1) pixels in the input grid. Consider pixels adjacent if they share an edge *or a corner* (8-way connectivity, not just 4-way).

2.  **Create Red Outer Border:** For each blue object, examine the pixels immediately surrounding it (8-way connectivity). If a surrounding pixel is yellow (4), *or* if the surrounding pixel is outside the bounds of the input grid, change that surrounding pixel to red (2).

3.  **Create Light Blue Inner Border:** For each blue object, identify its inner border. A pixel is part of the inner border if it is blue (1) and is 8-way adjacent to any pixel that is *not* blue (1). Change these inner border pixels to light blue (8).

4.  **Fill Interior with Gray:**  After creating the borders, change all remaining blue (1) pixels within each original blue object to gray (5).

5. **Preserve All Other Colors**: Ensure all other original pixels in the input remain at their input color.
"""

import numpy as np

def find_objects(grid, color):
    """Finds contiguous regions of the specified color using 8-way connectivity."""
    mask = (grid == color)
    rows, cols = grid.shape
    labeled_grid = np.zeros_like(grid)
    label_count = 0

    def dfs(r, c, label):
        """Depth-first search to label connected components (8-way)."""
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r, c] != color or labeled_grid[r, c] != 0:
            return
        labeled_grid[r, c] = label
        # Explore all 8 neighbors
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                dfs(r + dr, c + dc, label)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and labeled_grid[r, c] == 0:
                label_count += 1
                dfs(r, c, label_count)

    return labeled_grid, label_count

def get_8_neighbors(grid, r, c):
    """Gets the valid 8-way neighbors of a cell."""
    rows, cols = grid.shape
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbors.append((nr, nc))
    return neighbors

def get_outer_border_8way(input_grid, labeled_array, object_label):
    """
    Find the pixels that immediately surround the current blue object (8-way),
    *and* are not part of the object.
    """
    outer_border = []
    rows, cols = input_grid.shape
    object_pixels = []

    # first, find all pixels of this object
    for r in range(rows):
        for c in range(cols):
            if labeled_array[r,c] == object_label:
                object_pixels.append((r,c))

    # now find surrounding pixels, only if not part of the object
    for r, c in object_pixels:
        for nr, nc in get_8_neighbors(input_grid, r, c):
            if labeled_array[nr, nc] != object_label:
                outer_border.append((nr,nc))
    return outer_border
    
def get_inner_border_8way(grid, labeled_array, object_label):
    """Gets the inner border pixels of a labeled object (8-way)."""
    inner_border_pixels = []
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if labeled_array[r, c] == object_label:
                for nr, nc in get_8_neighbors(grid, r, c):
                    if labeled_array[nr, nc] != object_label:
                        inner_border_pixels.append((r, c))
                        break  # Stop checking neighbors once a border is found
    return inner_border_pixels


def transform(input_grid):
    """Transforms the input grid according to the observed rules."""
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # 1. Identify Blue Regions (8-way connectivity)
    labeled_array, num_blue_objects = find_objects(input_grid, 1)

    for i in range(1, num_blue_objects + 1):  # Iterate through each blue object
        # 2. Create Red Outer Border (8-way)
        outer_border = get_outer_border_8way(input_grid, labeled_array, i)
        for r, c in outer_border:
            # Check if the outer border pixel is yellow OR outside the grid
            if input_grid[r, c] == 4 or r < 0 or r >= rows or c < 0 or c >= cols:
                output_grid[r, c] = 2

        # 3. Create Light Blue Inner Border (8-way)
        inner_border_pixels = get_inner_border_8way(input_grid, labeled_array, i)
        for r, c in inner_border_pixels:
           output_grid[r,c] = 8

        # 4. Fill Central Area with Gray
        for r in range(rows):
            for c in range(cols):
                if labeled_array[r, c] == i and output_grid[r,c] == 1: # still blue in output
                    output_grid[r, c] = 5

    return output_grid
```