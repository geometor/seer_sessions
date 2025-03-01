"""
1.  **Identify Colored Regions:** Examine the input grid and identify all distinct colored regions (objects). Note their colors, heights, and widths.
2.  **Conditional Object Creation:**
    *   If a region has a height of 1 and is orange, magenta, or maroon, create a new region directly *below* it.
    *   The new region will have:
        *   Color: Green (3)
        *   Width: The same as the original region.
        *   Height: 1.
3.  **Preserve Other Regions:** All regions not matching the above criteria remain unchanged in color, position, and dimensions.
"""

import numpy as np

def find_objects(grid):
    """Finds contiguous objects of the same color in a grid."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, object_pixels):
        """Depth-first search to find all connected pixels of the same color."""
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        object_pixels.append((row, col))
        dfs(row + 1, col, color, object_pixels)
        dfs(row - 1, col, color, object_pixels)
        dfs(row, col + 1, color, object_pixels)
        dfs(row, col - 1, color, object_pixels)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col] and grid[row, col] != 0:
                object_pixels = []
                dfs(row, col, grid[row, col], object_pixels)
                if object_pixels:
                    objects.append({
                        'color': grid[row, col],
                        'pixels': object_pixels
                    })
    return objects

def get_object_dimensions(object_pixels):
    """Calculates the height and width of an object."""
    rows, cols = zip(*object_pixels)
    height = max(rows) - min(rows) + 1
    width = max(cols) - min(cols) + 1
    return height, width

def get_object_bottom_edge(object_pixels):
    """Finds the bottom edge of an object."""
    rows, cols = zip(*object_pixels)
    max_row = max(rows)
    bottom_edge = [(r, c) for r, c in object_pixels if r == max_row]
    bottom_edge.sort(key=lambda x: x[1])
    return bottom_edge

def transform(input_grid):
    # initialize output_grid
    output_grid = input_grid.copy()
    objects = find_objects(input_grid)

    # change output pixels 
    for obj in objects:
        color = obj['color']
        pixels = obj['pixels']
        height, width = get_object_dimensions(pixels)
        bottom_edge = get_object_bottom_edge(pixels)

        if height == 1 and color in [7, 6, 9]:  # Orange, Magenta, Maroon
            # Create a new green region below
            start_col = bottom_edge[0][1]
            end_col = bottom_edge[-1][1]
            new_row = bottom_edge[0][0] + 1
            if new_row < output_grid.shape[0]: # Check for grid boundaries
              for col in range(start_col, end_col + 1):
                  output_grid[new_row, col] = 3

    return output_grid