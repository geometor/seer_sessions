# 6d58a25d • 008 • refine_coder

---
```python
"""
The transformation identifies maroon (9) shapes in the input grid. It replaces the maroon pixels with azure (8) pixels.
Then, it extends the azure shape downwards. The extension has the same width as the original maroon shape, and its height is
equal to the height of the original maroon shape. Existing azure pixels are preserved.
"""

import numpy as np

def find_shapes(grid, color):
    """Finds all contiguous shapes of the specified color."""
    visited = np.zeros_like(grid, dtype=bool)
    shapes = []

    def dfs(row, col):
        """Depth-first search to find contiguous pixels."""
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
            visited[row, col] or grid[row, col] != color):
            return []
        
        visited[row, col] = True
        coords = [(row, col)]
        
        coords.extend(dfs(row + 1, col))
        coords.extend(dfs(row - 1, col))
        coords.extend(dfs(row, col + 1))
        coords.extend(dfs(row, col - 1))
        return coords

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col] and grid[row, col] == color:
                shape_coords = dfs(row, col)
                if shape_coords:
                    shapes.append(shape_coords)
    return shapes


def get_shape_dimensions(shape_coords):
    """Calculates the height and width of a shape given its coordinates."""
    if not shape_coords:
        return 0,0
    rows = [r for r, _ in shape_coords]
    cols = [c for _, c in shape_coords]
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)
    height = max_row - min_row + 1
    width = max_col - min_col + 1
    return (min_row, min_col), height, width

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid.
    output_grid = np.copy(input_grid)

    # Find existing azure pixels
    azure_pixels = np.argwhere(input_grid == 8)

    # Find all maroon shapes.
    maroon_shapes = find_shapes(input_grid, 9)
    
    for shape_coords in maroon_shapes:
        # Get dimensions of the current maroon shape.
        (min_row, min_col), maroon_height, maroon_width = get_shape_dimensions(shape_coords)

        # Replace maroon pixels with azure.
        for r, c in shape_coords:
            output_grid[r, c] = 8

        # Extend the azure shape downwards.
        for r in range(maroon_height):
           for c in range(maroon_width):
                output_grid[min_row + maroon_height + r, min_col + c] = 8
    
    # Preserve existing azure pixels.
    for row, col in azure_pixels:
        output_grid[row, col] = 8

    return output_grid
```
