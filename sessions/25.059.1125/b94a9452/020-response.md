# b94a9452 • 020 • refine_coder

---
```python
"""
1.  **Identify the Largest Object:** Find the largest contiguous block of pixels of the same color (excluding white/0) in the input grid. This contiguous block can be any shape - does not need to be rectangular.
2.  **Determine Object Color:** Note the color of the largest object.
3.  **Determine output size:**
    *   If the largest object in the input is color 1(blue) or 3(green) output is 5x5.
    *   If the largest object in the input is color 4 (yellow), output is 9x9.
4.  **Create Output Grid:** Create an output grid of the determined size.
5.  **Fill Background:** Fill the entire output grid with the object color.
6.  **Locate Center Pixel:** find the center pixel of the output grid
    *  For 5x5 grids, the center is at index `[2, 2]`.
    *  For 9x9 grids, the center is at index `[4, 4]`.
7.  **Set Center Pixel:**  Set the value/color of the center pixel of the output grid to `0` (white).
"""

import numpy as np

def find_largest_object(grid):
    """Finds the largest contiguous object in a grid, excluding color 0."""
    visited = np.zeros_like(grid, dtype=bool)
    max_size = 0
    object_coords = []
    object_color = 0

    def dfs(row, col, color, current_coords):
        """Depth-first search to find contiguous regions."""
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
        current_coords.append((row, col))
        size = 1
        size += dfs(row + 1, col, color, current_coords)
        size += dfs(row - 1, col, color, current_coords)
        size += dfs(row, col + 1, color, current_coords)
        size += dfs(row, col - 1, color, current_coords)
        return size

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col] and grid[row, col] != 0:
                current_coords = []
                size = dfs(row, col, grid[row, col], current_coords)
                if size > max_size:
                    max_size = size
                    object_coords = current_coords
                    object_color = grid[row,col]

    return object_coords, object_color

def transform(input_grid):
    # Find the largest object (excluding color 0) and its color
    object_coords, object_color = find_largest_object(input_grid)


    # Determine output size based on object color
    if object_color in [1, 3]:  # Blue or Green
        output_size = 5
    elif object_color == 4:  # Yellow
        output_size = 9
    else: # handle edge case where there is no object
       return np.zeros((1,1),dtype=int)

    # Create output grid and fill with object color
    output_grid = np.full((output_size, output_size), object_color, dtype=int)

    # Set center pixel to 0 (white)
    center_index = output_size // 2
    output_grid[center_index, center_index] = 0

    return output_grid
```
