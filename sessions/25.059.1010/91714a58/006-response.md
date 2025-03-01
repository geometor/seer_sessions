# 91714a58 • 006 • refine_coder

---
```python
"""
Identifies a red rectangle based on its spatial relationship with a multi-colored object. If a multi-colored object exists, the red rectangle that overlaps with its bounding box on the x and y axis is selected. Otherwise, the largest red rectangle is selected. The selected rectangle is preserved in the output grid, with all other pixels set to white.
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

def find_largest_red_rectangle(grid):
    """
    Finds the largest rectangle of red pixels within the grid.

    Returns:
        A tuple (start_row, start_col, end_row, end_col) defining the rectangle,
        or None if no red pixels are found.
    """
    red_pixels = np.argwhere(grid == 2)
    if len(red_pixels) == 0:
        return None

    max_area = 0
    best_rectangle = None

    for start_row, start_col in red_pixels:
        for end_row, end_col in red_pixels:
            if end_row >= start_row and end_col >= start_col:
                # Check if the rectangle is all red
                sub_grid = grid[start_row:end_row+1, start_col:end_col+1]
                if np.all(sub_grid == 2):
                    area = (end_row - start_row + 1) * (end_col - start_col + 1)
                    if area > max_area:
                        max_area = area
                        best_rectangle = (start_row, start_col, end_row, end_col)
    return best_rectangle

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

def overlaps(rect1, rect2):
    """
    Checks if two rectangles (bounding boxes) overlap on x and y projections.
    """
    start_row1, start_col1, end_row1, end_col1 = rect1
    start_row2, start_col2, end_row2, end_col2 = rect2
    
    # Check for x-axis overlap
    x_overlap = not (end_col1 < start_col2 or end_col2 < start_col1)

    # Check for y-axis overlap
    y_overlap = not (end_row1 < start_row2 or end_row2 < start_row1)
    
    return x_overlap and y_overlap


def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)

    # Find the multi-colored object
    multicolored_object = find_multicolored_object(input_grid)
    
    selected_rectangle = None

    if multicolored_object:
      # Find red rectangles
      red_rectangles = find_objects(input_grid, 2)
      # Check for overlaps
      for red_rect in red_rectangles:
          if overlaps(red_rect, multicolored_object):
              selected_rectangle = red_rect
              break # select the first that overlaps
    
    # if no multi-colored object, or no overlap
    if selected_rectangle is None:
        selected_rectangle = find_largest_red_rectangle(input_grid)
        
    # change output pixels 
    if selected_rectangle:
        start_row, start_col, end_row, end_col = selected_rectangle
        output_grid[start_row:end_row+1, start_col:end_col+1] = 2

    return output_grid.tolist()
```
