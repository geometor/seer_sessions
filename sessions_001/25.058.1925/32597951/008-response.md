# 32597951 • 008 • refine_coder

---
```python
"""
1.  **Identify Azure Regions:** Locate all contiguous regions of azure (8) pixels in the input grid. Pixels are considered part of the same region if they are adjacent horizontally or vertically.
2.  **Find Region Center:** For each identified azure region, determine its center. The center is the pixel that is part of the longest horizontal line of pixels in the shape, and longest vertical line of pixels in the shape. If there are two equal maximum length, the center lies between them.
3.  **Create Green Cross:** Transform the center pixel of each azure region to green (3). Extend the green color outwards from the center, creating a cross (+) shape. The extension continues only along connected azure pixels in each of the four cardinal directions (up, down, left, and right) until a non-azure pixel or the grid edge is encountered.
4.  **Preserve Other Pixels:** All pixels that are not part of any azure region, or part of a generated green cross, retain their original color values.
"""

import numpy as np

def find_contiguous_regions(grid, color):
    # Find all pixels of the specified color.
    pixels = np.argwhere(grid == color)
    if len(pixels) == 0:
        return []

    regions = []
    visited = set()

    for start_pixel in pixels:
        start_tuple = tuple(start_pixel)
        if start_tuple in visited:
            continue

        region = [start_tuple]
        queue = [start_tuple]
        visited.add(start_tuple)

        while queue:
            x, y = queue.pop(0)
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nx, ny = x + dx, y + dy
                neighbor_tuple = (nx, ny)
                if (0 <= nx < grid.shape[0] and 0 <= ny < grid.shape[1] and
                    grid[nx, ny] == color and neighbor_tuple not in visited):
                    region.append(neighbor_tuple)
                    queue.append(neighbor_tuple)
                    visited.add(neighbor_tuple)
        regions.append(region)

    return regions

def find_center(region):
    # Find the longest horizontal and vertical lines within the region.
    xs = [p[0] for p in region]
    ys = [p[1] for p in region]

    max_horizontal_length = 0
    max_vertical_length = 0
    horizontal_center = None
    vertical_center = None

    for x in sorted(list(set(xs))):
        row = [p for p in region if p[0] == x]
        row.sort(key=lambda p: p[1])  # Sort by y-coordinate
        for i in range(len(row)):
            current_length = 1
            for j in range(i + 1, len(row)):
                if row[j][1] == row[j-1][1] + 1:
                    current_length += 1
                else:
                    break
            if current_length > max_horizontal_length:
                max_horizontal_length = current_length
                center_y_index = i + current_length // 2
                horizontal_center = (x, row[center_y_index][1])

    for y in sorted(list(set(ys))):
        col = [p for p in region if p[1] == y]
        col.sort(key=lambda p: p[0])
        for i in range(len(col)):
            current_length = 1
            for j in range(i + 1, len(col)):
                if col[j][0] == col[j-1][0] + 1:
                    current_length += 1
                else:
                    break
            if current_length > max_vertical_length:
                max_vertical_length = current_length
                center_x_index = i + current_length // 2
                vertical_center = (col[center_x_index][0], y)

    #The intersection is the center.
    if horizontal_center and vertical_center and horizontal_center[0] == vertical_center[0]:
       return horizontal_center

    if horizontal_center is None:
        return vertical_center
    if vertical_center is None:
        return horizontal_center
    #If they don't intersect, take closest.
    min_dist = 10000
    best_center = None
    for x,y in region:
       dist = abs(x- horizontal_center[0]) + abs(y - vertical_center[1])
       if dist < min_dist:
            min_dist = dist
            best_center = (x,y)

    return best_center

def create_cross(grid, center, region):
    # Create the cross by extending outwards from the center.
    if not center:
      return
    
    x, y = center
    grid[x, y] = 3  # Set center to green

    # Extend up
    for i in range(x - 1, -1, -1):
        if (i, y) in region:
            grid[i, y] = 3
        else:
            break

    # Extend down
    for i in range(x + 1, grid.shape[0]):
        if (i, y) in region:
            grid[i, y] = 3
        else:
            break

    # Extend left
    for j in range(y - 1, -1, -1):
        if (x, j) in region:
            grid[x, j] = 3
        else:
            break

    # Extend right
    for j in range(y + 1, grid.shape[1]):
        if (x, j) in region:
            grid[x, j] = 3
        else:
            break


def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    # Find azure regions.
    azure_regions = find_contiguous_regions(input_grid, 8)

    # Process each azure region.
    for region in azure_regions:
        # Find the center of the region.
        center = find_center(region)

        # Create the green cross within the region.
        create_cross(output_grid, center, region)

    return output_grid
```
