# 00d62c1b • 020 • refine_coder

---
```python
"""
1.  **Identify the Largest Object:** Find the largest contiguous block of green (3) pixels in the input grid. This is the target object.

2.  **Determine Interior Pixels:** Accurately identify the *interior* pixels of the target object. A pixel is considered inside if it's part of the largest green object and is completely surrounded by other green pixels of that *same* object, such that it cannot be reached from the background without crossing a green pixel of the target object. A simple neighbor check is insufficient; a flood-fill or similar approach from the outside edge of the grid is needed to ensure accurate identification of enclosed regions.

3.  **Change Interior Color:** Change the color of all identified *interior* pixels of the target object from green (3) to yellow (4).

4. **Preserve Other Pixels:** All other pixels in the grid that are not part of the target object's interior remain unchanged.
"""

import numpy as np

def find_largest_object(grid, color):
    visited = np.zeros_like(grid, dtype=bool)
    max_size = 0
    largest_object_coords = []

    def dfs(row, col, current_object_coords):
        if (
            row < 0
            or row >= grid.shape[0]
            or col < 0
            or col >= grid.shape[1]
            or visited[row, col]
            or grid[row, col] != color
        ):
            return 0

        visited[row, col] = True
        current_object_coords.append((row, col))
        size = 1
        size += dfs(row + 1, col, current_object_coords)
        size += dfs(row - 1, col, current_object_coords)
        size += dfs(row, col + 1, current_object_coords)
        size += dfs(row, col - 1, current_object_coords)
        return size

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and not visited[row, col]:
                current_object_coords = []
                current_size = dfs(row, col, current_object_coords)
                if current_size > max_size:
                    max_size = current_size
                    largest_object_coords = current_object_coords

    return largest_object_coords

def flood_fill(grid, row, col, target_color, replacement_color):
    """
    Performs a flood fill on the grid, starting from (row, col).
    Only fills pixels that are equal to target_color.
    """
    if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
            grid[row, col] != target_color):
        return
    grid[row, col] = replacement_color
    flood_fill(grid, row + 1, col, target_color, replacement_color)
    flood_fill(grid, row - 1, col, target_color, replacement_color)
    flood_fill(grid, row, col + 1, target_color, replacement_color)
    flood_fill(grid, row, col - 1, target_color, replacement_color)

def find_interior_pixels(grid, object_coords, object_color):
    """
    Identifies the interior pixels of an object using a flood-fill approach.
    """
    # Create a copy of the grid to work with
    temp_grid = np.copy(grid)

    # Replace the object with a temporary color
    temp_object_color = -1  # Use a color that doesn't exist in the original grid
    for row, col in object_coords:
        temp_grid[row, col] = temp_object_color

    # Find background color (assuming the top-left corner is background)
    background_color = temp_grid[0, 0]


    # Flood fill the background from the edges with a different temporary color
    temp_background_color = -2
    if background_color != temp_object_color:
        flood_fill(temp_grid, 0, 0, background_color, temp_background_color)

    # Identify interior pixels: they are the remaining temp_object_color pixels
    interior_pixels = []
    for row, col in object_coords:
        if temp_grid[row, col] == temp_object_color:
            interior_pixels.append((row, col))

    return interior_pixels

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # find largest green object
    green_object_coords = find_largest_object(input_grid, 3)

    # find interior pixels of the largest green object
    interior_pixels = find_interior_pixels(input_grid, green_object_coords, 3)

    # change interior object pixels to yellow
    for row, col in interior_pixels:
        output_grid[row, col] = 4
        
    return output_grid
```
