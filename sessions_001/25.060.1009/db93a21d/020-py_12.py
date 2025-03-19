"""
1.  **Find Maroon Rectangles:** Identify all rectangular objects of color maroon (9) in the input grid.
2.  **Outline Maroon Rectangles:** Draw a green (3) outline, one pixel thick, around each identified maroon rectangle.
3.  **Add Blue Rectangle:** Add a new blue (1) rectangle of size 4x7 to the top of the grid, starting on the third row.
4.  **Outline Blue Rectangle:** Draw a green (3) outline, one pixel thick, around the newly added blue rectangle. The rectangle should fill the area defined, even if that requires reducing the size.
5.  **Fill Adjacent Pixels:** Change the color of any white (0) pixels that are directly adjacent (up, down, left, or right, but not diagonally) to a green (3) pixel to green (3).
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
    for x in range(min_x - 1, max_x + 2):
        if 0 <= x < grid.shape[0] and 0 <= min_y - 1 < grid.shape[1]:
            grid[x, min_y - 1] = color
        if 0 <= x < grid.shape[0] and 0 <= max_y + 1 < grid.shape[1]:
            grid[x, max_y + 1] = color

def add_new_rectangle(grid, top_left, size, color):
    """Adds a new rectangle to the grid, adjusting size if necessary."""
    width, height = size
    start_x, start_y = top_left
    for x in range(start_x, min(start_x + height, grid.shape[0])):
        for y in range(start_y, min(start_y + width, grid.shape[1])):
            grid[x, y] = color

def fill_adjacent(grid, color, target_color):
    """Fills pixels of target_color adjacent to 'color' with 'color'."""
    new_grid = grid.copy()
    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            if grid[x, y] == target_color:
                # Check neighbors
                for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < grid.shape[0] and 0 <= ny < grid.shape[1] and grid[nx, ny] == color:
                        new_grid[x, y] = color
                        break
    return new_grid


def transform(input_grid):
    """Transforms the input grid according to the described rules."""
    output_grid = input_grid.copy()

    # 1. Find maroon rectangles
    maroon_rectangles = find_objects(output_grid, 9)

    # 2. Outline maroon rectangles with green
    for top_left, bottom_right in maroon_rectangles:
        outline_rectangle(output_grid, top_left, bottom_right, 3)

    # 3. Add a new blue rectangle (4x7) at the top of grid, starting row 2 (index)
    add_new_rectangle(output_grid, (2, 0), (7, 4), 1)  # start_x = 2, start_y = 0

    # 4. Outline blue rectangle. Get max_y from blue object, or if it was truncated,
    # then the height-1
    blue_rectangles = find_objects(output_grid, 1)
    for top_left, bottom_right in blue_rectangles:
        outline_rectangle(output_grid, top_left, bottom_right, 3)


    # 5. Fill adjacent white pixels with green.
    output_grid = fill_adjacent(output_grid, 3, 0)
    
    return output_grid