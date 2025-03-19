# 264363fd • 018 • refine_coder

---
```python
"""
The transformation identifies the largest green region, moves a 3x3 structure within it, and replaces the border of the green region with grey.
"""

import numpy as np

def find_objects(grid, color):
    """Finds contiguous objects of a given color."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def is_valid(x, y):
        return 0 <= x < grid.shape[0] and 0 <= y < grid.shape[1]

    def dfs(x, y):
        if not is_valid(x, y) or visited[x, y] or grid[x, y] != color:
            return []

        visited[x, y] = True
        object_pixels = [(x, y)]

        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            object_pixels.extend(dfs(x + dx, y + dy))

        return object_pixels

    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            if grid[x, y] == color and not visited[x, y]:
                objects.append(dfs(x, y))

    return objects

def find_largest_region(regions):
    """Finds the region with the maximum number of pixels."""
    if not regions:
        return []
    return max(regions, key=len)

def get_border(pixels, grid_shape):
    """Gets the border pixels of a region."""
    border_pixels = []
    for x, y in pixels:
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if not (0 <= nx < grid_shape[0] and 0 <= ny < grid_shape[1]):
                continue

            if (nx, ny) not in pixels:
                border_pixels.append((x,y))
                break
    return border_pixels
    
def find_structure(grid):
    """Finds the 3x3 structure in the grid.  Improved to be less fragile."""
    for x in range(1, grid.shape[0] - 1):
        for y in range(1, grid.shape[1] - 1):
            pixels = [(x + dx, y + dy) for dx in range(-1, 2) for dy in range(-1, 2)]
            # Check if all pixels are within bounds
            if all(0 <= px < grid.shape[0] and 0 <= py < grid.shape[1] for px, py in pixels):
                return pixels
    return []

def move_structure(grid, structure, region):
    """Moves the structure to the region, handling overflow."""
    min_x = min([x for x, y in region])
    max_x = max([x for x, y in region])
    min_y = min([y for x, y in region])
    max_y = max([y for x, y in region])

    struct_height = 3  # Fixed size of 3x3
    struct_width = 3   # Fixed size of 3x3

    new_x = min_x + 1
    new_y = min_y + 1

    # Adjust for overflow
    new_x = min(new_x, max_x - struct_height + 1)
    new_y = min(new_y, max_y - struct_width + 1)

    structure_origin = structure[0]
    moved_structure = [(x - structure_origin[0] + new_x, y - structure_origin[1] + new_y) for x, y in structure]

    return moved_structure

def should_clean_original(structure, grid):
    """
    Checks if original structure should be cleaned based on the color
    diversity
    """
    colors = set()
    for x,y in structure:
        colors.add(grid[x,y])
    
    return len(colors) > 3

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # Find green regions
    green_regions = find_objects(input_grid, 3)
    
    # Find the largest Green Region
    largest_region = find_largest_region(green_regions)


    #find the structure
    structure = find_structure(input_grid)


    #find and move structure
    if len(structure) > 0 and len(largest_region) > 0:

      moved_struct = move_structure(input_grid, structure, largest_region)
      #clean old structure position
      if should_clean_original(structure, input_grid):
        for x, y in structure:
          output_grid[x,y] = 4

      #paint in new position
      color_struct = [input_grid[x,y] for x,y in structure]

      for i, pos in enumerate(moved_struct):
          output_grid[pos] =  color_struct[i]


    # Get the border pixels of the largest region
    border = get_border(largest_region, input_grid.shape)

    # Replace the border pixels with grey.
    for x, y in border:
        output_grid[x,y] = 5

    return output_grid
```
