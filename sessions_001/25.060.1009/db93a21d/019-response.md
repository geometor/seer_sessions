# db93a21d • 019 • refine_coder

---
```python
"""
1.  **Find Maroon Rectangles:** Locate all rectangular shapes of maroon (9) color within the input grid.
2.  **Outline Maroon Rectangles:** Draw a green (3) border around each of the maroon rectangles found in the previous step. The outline should extend one pixel beyond the edges of the original rectangle on all sides.
3.  **Add Blue Rectangle:** Create a new blue (1) rectangle with a fixed height of 4 and width of 7, The top-left corner is located at row 3, column 2 (using 0-based indexing).
4.  **Outline Blue Rectangle**: Draw a green border around the blue rectangle.
5.  **Fill Adjacent White:** Change the color of any white (0) pixels that are directly adjacent (up, down, left, or right) to a green (3) pixel to green (3).
"""

import numpy as np

def find_objects(grid, color):
    """Finds rectangular objects of a specific color in the grid."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def is_valid(x, y):
        return 0 <= x < grid.shape[0] and 0 <= y < grid.shape[1]

    def dfs(x, y, obj):
        if not is_valid(x, y) or visited[x, y] or grid[x, y] != color:
            return
        visited[x, y] = True
        obj.append((x, y))
        dfs(x + 1, y, obj)
        dfs(x - 1, y, obj)
        dfs(x, y + 1, obj)
        dfs(x, y - 1, obj)

    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            if grid[x, y] == color and not visited[x, y]:
                obj = []
                dfs(x, y, obj)
                # Determine if the found object is a rectangle, and get its boundaries.
                if obj:
                    xs, ys = zip(*obj)
                    min_x, max_x = min(xs), max(xs)
                    min_y, max_y = min(ys), max(ys)
                    # Check if it is really a rectangle
                    if all(grid[i,j] == color for i in range(min_x, max_x + 1) for j in range(min_y, max_y+1)):
                        objects.append(((min_x, min_y), (max_x, max_y))) # Store as top-left and bottom-right corners
    return objects

def outline_rectangle(grid, top_left, bottom_right, color):
    """Outlines a rectangle defined by top_left and bottom_right with the specified color."""
    min_x, min_y = top_left
    max_x, max_y = bottom_right

    # Top and bottom borders
    for y in range(min_y - 1, max_y + 2):
        if 0 <= min_x - 1 < grid.shape[0] and 0 <= y < grid.shape[1]:
            grid[min_x - 1, y] = color
        if 0 <= max_x + 1 < grid.shape[0] and 0 <= y < grid.shape[1]:
            grid[max_x + 1, y] = color

    # Left and right borders
    for x in range(min_x, max_x + 1):
        if 0 <= x < grid.shape[0] and 0 <= min_y - 1 < grid.shape[1]:
            grid[x, min_y - 1] = color
        if 0 <= x < grid.shape[0] and 0 <= max_y + 1 < grid.shape[1]:
            grid[x, max_y + 1] = color

def add_new_rectangle(grid, top_left, size, color):
   """Adds a new rectangle to the grid."""
   width, height = size
   start_x, start_y = top_left
   for x in range(start_x, start_x + height):
        for y in range(start_y, start_y + width):
            if 0 <= x < grid.shape[0] and 0 <= y < grid.shape[1]:
                grid[x,y] = color

def fill_adjacent(grid, color, target_color):
    """Fills pixels of target_color adjacent to 'color' with 'color'."""
    new_grid = grid.copy()  # Work on a copy to avoid modifying during iteration
    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            if grid[x,y] == target_color:
                # Check neighbors
                for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < grid.shape[0] and 0 <= ny < grid.shape[1] and grid[nx, ny] == color:
                        new_grid[x, y] = color
                        break  # Only fill once per cell
    return new_grid

def transform(input_grid):
    # initialize output_grid
    output_grid = input_grid.copy()

    # 1. Find Maroon Rectangles
    maroon_rectangles = find_objects(output_grid, 9)

    # 2. Outline Maroon Rectangles
    for top_left, bottom_right in maroon_rectangles:
        outline_rectangle(output_grid, top_left, bottom_right, 3)

    # 3. Add Blue Rectangle
    add_new_rectangle(output_grid, (2, 1), (4, 7), 1)

    # 4. Outline Blue Rectangle
    blue_rectangles = find_objects(output_grid, 1)
    for top_left, bottom_right in blue_rectangles:
        outline_rectangle(output_grid, top_left, bottom_right, 3)


    # 5. Fill Adjacent White
    output_grid = fill_adjacent(output_grid, 3, 0)

    return output_grid
```
