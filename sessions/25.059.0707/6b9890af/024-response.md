# 6b9890af • 024 • refine_coder

---
```python
"""
1.  **Identify the Target Object:** Find the largest contiguous object in the input grid, *excluding* black (0) and red (2) pixels. If multiple objects are present and not contiguous, select the largest one.
2.  **Create Bounding Box:** Determine the smallest rectangular box that completely encloses the target object.
3.  **Generate Output Grid:** Create a new grid with the dimensions of the bounding box, plus a 1-pixel border on all sides.
4. **Copy the object:** Copy the target object from the original grid to the new grid, maintaining its relative position within the bounding box.
5.  **Add Red Border:** Fill the outermost rows and columns of the new grid with red (2) pixels, creating a border around the copied object.
"""

import numpy as np

def find_largest_contiguous_object(grid):
    """
    Finds the largest contiguous object in the grid, excluding black (0) and red (2).
    Returns a list of (row, col) coordinates of the object.
    """
    visited = set()
    max_size = 0
    largest_object = []

    def dfs(row, col, color):
        if (row, col) in visited or not (0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]) or grid[row, col] != color:
            return []
        visited.add((row, col))
        coords = [(row, col)]
        coords += dfs(row + 1, col, color)
        coords += dfs(row - 1, col, color)
        coords += dfs(row, col + 1, color)
        coords += dfs(row, col - 1, color)
        return coords

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if (row, col) not in visited and grid[row, col] != 0 and grid[row, col] != 2:
                color = grid[row, col]
                object_coords = dfs(row, col, color)
                if len(object_coords) > max_size:
                    max_size = len(object_coords)
                    largest_object = object_coords
    return largest_object

def get_bounding_box(coords):
    """
    Calculates the bounding box for a list of coordinates.
    Returns (min_row, max_row, min_col, max_col).
    """
    if not coords:
        return 0, -1, 0, -1  # Handle empty list
    min_row = min(r for r, c in coords)
    max_row = max(r for r, c in coords)
    min_col = min(c for r, c in coords)
    max_col = max(c for r, c in coords)
    return min_row, max_row, min_col, max_col

def transform(input_grid):
    # Find the largest contiguous object (excluding black and red)
    largest_object_coords = find_largest_contiguous_object(input_grid)

    # Get the bounding box
    min_row, max_row, min_col, max_col = get_bounding_box(largest_object_coords)

    # Create the output grid with a 1-pixel border
    output_height = max_row - min_row + 3
    output_width = max_col - min_col + 3
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Copy the object to the output grid
    for r, c in largest_object_coords:
        output_grid[r - min_row + 1, c - min_col + 1] = input_grid[r, c]

    # Add the red border
    output_grid[0, :] = 2
    output_grid[-1, :] = 2
    output_grid[:, 0] = 2
    output_grid[:, -1] = 2

    return output_grid
```
