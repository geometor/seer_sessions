# 91714a58 • 008 • refine_coder

---
```python
"""
Identifies a specific red rectangle within the input grid and preserves it in the output grid, setting all other pixels to white. The selection criteria for the red rectangle are not solely based on size or overlap with a multi-colored object (if present) but involve a more complex spatial relationship that needs to be determined through further analysis of the examples.
"""

import numpy as np

def find_objects(grid, color):
    """
    Finds all contiguous objects of a specified color in the grid.
    Returns a list of bounding box tuples (start_row, start_col, end_row, end_col).
    """
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col):
        """Depth-first search to find contiguous pixels."""
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
                region = dfs(row, col)
                if region:
                    min_row = min(r[0] for r in region)
                    max_row = max(r[0] for r in region)
                    min_col = min(r[1] for r in region)
                    max_col = max(r[1] for r in region)
                    objects.append((min_row, min_col, max_row, max_col))
    return objects

def find_multicolored_object(grid):
    """
    Finds a single contiguous object composed of multiple colors (excluding red).

    Returns:
      A bounding box (start_row, start_col, end_row, end_col), or None.
    """
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, start_color):
        """Depth-first search to find contiguous pixels."""
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] == 2): # Exclude red
            return []

        visited[row, col] = True
        region = [(row, col)]
        current_color = grid[row,col]

        region.extend(dfs(row + 1, col, start_color))
        region.extend(dfs(row - 1, col, start_color))
        region.extend(dfs(row, col + 1, start_color))
        region.extend(dfs(row, col - 1, start_color))
        return region

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] != 2 and not visited[row, col]:  # Exclude red and visited
                start_color = grid[row,col]
                region = dfs(row, col, start_color)
                if region:
                    colors_present = set()
                    for r,c in region:
                      colors_present.add(grid[r,c])
                    if len(colors_present) > 1:
                      min_row = min(r[0] for r in region)
                      max_row = max(r[0] for r in region)
                      min_col = min(r[1] for r in region)
                      max_col = max(r[1] for r in region)
                      return (min_row, min_col, max_row, max_col) # Return immediately upon finding one
    return None

def calculate_distance(rect1, rect2):
    """
    Calculates the minimum distance between two rectangles.
    """
    start_row1, start_col1, end_row1, end_col1 = rect1
    start_row2, start_col2, end_row2, end_col2 = rect2

    # Calculate centers of rectangles
    center_x1 = (start_col1 + end_col1) / 2
    center_y1 = (start_row1 + end_row1) / 2
    center_x2 = (start_col2 + end_col2) / 2
    center_y2 = (start_row2 + end_row2) / 2

    # Calculate distance between centers
    center_distance = np.sqrt((center_x1 - center_x2)**2 + (center_y1 - center_y2)**2)

    return center_distance

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)

    # Find all red rectangles
    red_rectangles = find_objects(input_grid, 2)

    # Find the multi-colored object (if it exists)
    multicolored_object = find_multicolored_object(input_grid)

    selected_rectangle = None

    if multicolored_object:
        # If a multi-colored object exists, find the red rectangle with minimum distance
        min_distance = float('inf')
        for red_rect in red_rectangles:
            distance = calculate_distance(red_rect, multicolored_object)
            if distance < min_distance:
                min_distance = distance
                selected_rectangle = red_rect
    else:
        # if no multi colored object - still need to pick one
        # Placeholder: select the first red rectangle found.  This is WRONG and needs to be updated.
        if red_rectangles:
          selected_rectangle = red_rectangles[0]

    # change output pixels
    if selected_rectangle:
        start_row, start_col, end_row, end_col = selected_rectangle
        output_grid[start_row:end_row+1, start_col:end_col+1] = 2

    return output_grid.tolist()
```
