# 22168020 • 010 • example_2 • investigate_coder

---
```python
"""
The transformation takes each colored shape (blue or yellow) and stretches it
out sideways as far as it can go within the bounds of the grid, overwriting any
white pixels (0) in its path, while preserving original y coordinates.
"""

import numpy as np

def get_regions(grid, colors):
    # find regions of specific colors in a grid
    regions = {}
    for color in colors:
        regions[color] = []
        visited = np.zeros_like(grid, dtype=bool)
        rows, cols = grid.shape
        for r in range(rows):
            for c in range(cols):
                if grid[r, c] == color and not visited[r, c]:
                    region = []
                    stack = [(r, c)]
                    while stack:
                        row, col = stack.pop()
                        if 0 <= row < rows and 0 <= col < cols and grid[row, col] == color and not visited[row, col]:
                            visited[row, col] = True
                            region.append((row, col))
                            stack.extend([(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)])
                    regions[color].append(region)
    return regions

def expand_region_horizontally(grid, region, color):
    # expand each region horizontally to grid edges or non-white cell
    min_y = min(r[0] for r in region)
    max_y = max(r[0] for r in region)
    min_x = min(r[1] for r in region)
    max_x = max(r[1] for r in region)

    # Find leftmost expansion limit
    left_limit = 0
    for x in range(min_x - 1, -1, -1):
        if any(grid[y,x] != 0 for y in range(min_y, max_y+1)):
            left_limit = x+1
            break

    # Find rightmost expansion limit
    right_limit = grid.shape[1] - 1
    for x in range(max_x + 1, grid.shape[1]):
        if any(grid[y,x] != 0 for y in range(min_y, max_y + 1)):
           right_limit = x-1
           break

    # expand by iterating each y coordinate to fill
    for y in range(min_y, max_y + 1):
        for x in range(left_limit, right_limit + 1):
             grid[y,x] = color
    return grid

def transform(input_grid):
    """Transforms the input grid according to the described rule."""

    # Convert input_grid to a NumPy array
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)


    # Identify Regions of blue and yellow.
    regions = get_regions(input_grid, [1, 4])


    # expand blue regions
    for region in regions[1]:
        output_grid = expand_region_horizontally(output_grid, region, 1)

    # expand yellow regions
    for region in regions[4]:
        output_grid = expand_region_horizontally(output_grid, region, 4)


    return output_grid.tolist()
```
