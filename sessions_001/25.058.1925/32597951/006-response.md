# 32597951 • 006 • refine_coder

---
```python
"""
1.  **Identify Azure Regions:** Find all regions of azure (8) pixels in the input grid.  Regions can be of any shape and size, and pixels are considered part of a region if they are adjacent horizontally or vertically. There may be multiple disjunct regions.
2.  **Find the Center of Each Region:** For *each* azure region, find the "center" of the cross. The center is at the intersection point of the longest horizontal line of azure pixels and the longest vertical line of azure pixels within that region.
3. **Create the Green Cross:** From the identified center, change azure pixels to green (3) to create a cross (+) shape. The cross extends outwards from the center, *following the existing azure pixels*. The length of each arm of the cross is determined by the extent of the contiguous azure pixels in each of the four cardinal directions (up, down, left, right) from the center.
4. **Preserve Other Pixels:** All pixels that are not part of the azure regions, or part of the subsequently formed green crosses, remain unchanged.
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
