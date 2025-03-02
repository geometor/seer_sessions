# db93a21d • 002 • example_4 • investigate_coder

---
```python
"""
1.  **Identify Maroon Rectangles:** Locate all rectangular objects of color 9 (maroon) in the input grid.
2.  **Create Green Outline:** For each identified maroon rectangle, create a 1-pixel thick outline of color 3 (green) around it. The outline expands the rectangle by one cell in all directions (up, down, left, right).
3.  **Create Blue Infill:** The fill color is 1 (blue).
    *   It fills under the area defined by the green outline, on the bottom
    *   The infill area has the width of the green outline.
    *   The blue infill extends all the way down to the bottom of the output.
    *   If maroon is in the top two rows, create an infill block the width of the green outline all the way up to the top.
"""

import numpy as np

def find_objects(grid, color):
    # Find all objects of a specific color in the grid.
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col):
        # Depth-first search to find contiguous regions of the same color.
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
                # Approximate a rectangle.
                if region:
                  min_row = min(r for r, _ in region)
                  max_row = max(r for r, _ in region)
                  min_col = min(c for _, c in region)
                  max_col = max(c for _, c in region)

                  objects.append(((min_row, min_col), (max_row, max_col)))
    return objects

def create_outline(output_grid, top_left, bottom_right, color):
    # Create a 1-pixel thick outline around the specified rectangle.
    min_row, min_col = top_left
    max_row, max_col = bottom_right

    for r in range(min_row - 1, max_row + 2):
        for c in range(min_col - 1, max_col + 2):
            if (0 <= r < output_grid.shape[0] and 0 <= c < output_grid.shape[1] and
                (r == min_row - 1 or r == max_row + 1 or c == min_col - 1 or c == max_col + 1)):
                output_grid[r, c] = color

def create_infill(output_grid, top_left, bottom_right, color):
    # Create a rectangular infill below (and optionally above) the outlined object.
    min_row, min_col = top_left
    max_row, max_col = bottom_right

    # Infill below
    for r in range(max_row + 1, output_grid.shape[0]):
        for c in range(min_col -1, max_col + 2):
            if 0 <= r < output_grid.shape[0] and 0 <= c < output_grid.shape[1]:
                output_grid[r,c] = color
    # Infill above if in top two rows.
    if min_row <= 2:
        for r in range(0, min_row -1):
             for c in range(min_col -1, max_col + 2):
                if 0 <= r < output_grid.shape[0] and 0 <= c < output_grid.shape[1]:
                    output_grid[r,c] = color


def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)

    # Find maroon rectangles.
    maroon_objects = find_objects(input_grid, 9)

    # Apply transformations for each maroon rectangle.
    for top_left, bottom_right in maroon_objects:
      # Create green outline.
      create_outline(output_grid, top_left, bottom_right, 3)

    for top_left, bottom_right in maroon_objects:

      #create blue infill based upon outline
      create_infill(output_grid, top_left, bottom_right, 1)

    #copy existing pixels - all of them
    for r in range(input_grid.shape[0]):
      for c in range(input_grid.shape[1]):
        if output_grid[r,c] == 0 and input_grid[r,c] == 9:
          output_grid[r,c] = 9

    return output_grid
```
