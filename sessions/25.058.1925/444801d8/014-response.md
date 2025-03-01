# 444801d8 • 014 • refine_coder

---
```python
"""
1.  **Identify Background:** Determine the most frequent color in the input grid and designate it as the background color.

2.  **Identify Blue Objects:** Find all distinct, contiguous regions of blue (1) pixels.  A contiguous region is defined as a group of blue pixels connected horizontally or vertically.

3.  **Sort by Vertical Position:** Order the identified blue objects from top to bottom based on the row index of their topmost pixel.

4.  **Topmost Object Outline:** For the topmost blue object, change the color of any pixels that are directly adjacent (horizontally or vertically) to the blue object, *and not* blue (1) or background colored to red (2).

5.  **Bottommost Object Outline:** For the bottommost blue object, change the color of any pixels that are directly adjacent (horizontally or vertically) to the blue object, *and not* blue (1) or background colored to green (3).

6.  **Overlap Resolution:** If a pixel would be changed by *both* the topmost and bottommost outline operations, do *not* modify its color (leave it as it was in the input).
"""

import numpy as np

def get_objects(grid, color):
    """
    Find connected regions of a specific color.
    """
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    def dfs(row, col):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return []

        visited[row, col] = True
        region = [(row, col)]

        region.extend(dfs(row + 1, col))
        region.extend(dfs(row - 1, col))
        region.extend(dfs(row, col + 1))
        region.extend(dfs(row, col - 1))

        return region

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and not visited[row, col]:
                objects.append(dfs(row, col))
    return objects

def get_outline(grid, object_pixels, background_color):
    """
    Find the outline pixels of an object, excluding background.
    """
    outline = set()
    for row, col in object_pixels:
        neighbors = [(row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)]
        for n_row, n_col in neighbors:
            if (0 <= n_row < grid.shape[0] and 0 <= n_col < grid.shape[1] and
                    grid[n_row, n_col] != 1 and grid[n_row, n_col] != background_color):
                outline.add((n_row, n_col))
    return list(outline)

def transform(input_grid):
    # Initialize output grid
    output_grid = np.copy(input_grid)

    # Find the most frequent color (background)
    colors, counts = np.unique(input_grid, return_counts=True)
    background_color_index = np.argmax(counts)
    background_color = colors[background_color_index]

    # Find blue objects
    blue_objects = get_objects(input_grid, 1)

    # Sort blue objects by topmost row
    blue_objects.sort(key=lambda obj: min(pixel[0] for pixel in obj))

    # Get outlines, excluding background pixels
    outlines = []
    for obj in blue_objects:
        outlines.append(get_outline(input_grid, obj, background_color))

    # Topmost object outline
    if len(blue_objects) > 0:
        top_outline = outlines[0]
        for row, col in top_outline:
            output_grid[row, col] = 2

    # Bottommost object outline, handle overlap
    if len(blue_objects) > 1:
        bottom_outline = outlines[-1]
        for row, col in bottom_outline:
            if (row, col) not in (top_outline if len(blue_objects)>0 else []):  # Check for overlap
                output_grid[row, col] = 3

    return output_grid
```
