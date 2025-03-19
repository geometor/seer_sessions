"""
Creates a 6x6 grid representing the outline of an azure object within a frame.

1.  **Create Output Grid:** Initialize a 6x6 grid filled with 0 (white).
2.  **Draw Frame:** Draw a frame on the output grid:
    *   Yellow (4) line across the top (columns 1-4).
    *   Red (2) line down the left side (rows 1-4).
    *   Blue (1) line down the right side (rows 1-4).
    *   Green (3) line across the bottom (columns 1-4).
3.  **Find Azure Object:** Identify the contiguous region of azure (8) pixels in the input grid.
4.  **Trace Outline:** Trace the *outer* outline of the azure object, proceeding clockwise from the top-leftmost azure pixel. Consider only pixels on the external boundary.
5.  **Scale and Map Outline:**
    *   Determine the bounding box of the azure object in the input grid (min/max row and column).
    *   Map the outline coordinates to the inner 4x4 region of the output grid (rows 1-4, columns 1-4). Scale proportionally based on the bounding box dimensions.
6. **Place Azure:** set the value of the scaled and mapped outline coordinates to azure (8).
"""

import numpy as np

def find_objects(grid, color):
    """Finds coordinates of objects with a specific color."""
    coords = []
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i, j] == color:
                coords.append((i, j))
    return coords

def trace_outline(grid, start):
    """Traces the *outer* boundary of an object starting from a given point."""
    outline = []
    visited = set()
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Clockwise: Right, Down, Left, Up

    def is_valid(x, y, grid):
        return 0 <= x < grid.shape[0] and 0 <= y < grid.shape[1]

    def is_outline(x, y, grid, color):
        """Checks if a pixel is on the outer boundary."""
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if not is_valid(nx, ny, grid) or grid[nx, ny] != color:
                return True
        return False

    def dfs(x, y, grid, color):
        if (x, y) in visited or not is_valid(x, y, grid) or grid[x, y] != color:
            return

        visited.add((x, y))

        if is_outline(x, y, grid, color):
            outline.append((x, y))

        # Continue DFS in clockwise order, prioritizing outline pixels
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if is_valid(nx, ny, grid) and grid[nx, ny] == color and is_outline(nx, ny, grid, color) and (nx, ny) not in visited:
                dfs(nx, ny, grid, color) # explore neighbors
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if is_valid(nx,ny, grid) and grid[nx,ny] == color and (nx, ny) not in visited:
               dfs(nx, ny, grid, color)


    dfs(start[0], start[1], grid, grid[start[0], start[1]]) # use starting color
    return outline

def draw_frame(grid):
    """Draws the frame on the output grid."""
    grid[0, 1:5] = 4  # Yellow top
    grid[1:5, 0] = 2  # Red left
    grid[1:5, 5] = 1  # Blue right
    grid[5, 1:5] = 3  # Green bottom

def transform(input_grid):
    """Transforms the input grid according to the defined rules."""
    output_grid = np.zeros((6, 6), dtype=int)

    # Draw Frame
    draw_frame(output_grid)

    # Find Azure Object
    azure_coords = find_objects(input_grid, 8)

    # Trace Outline and Scale/Map
    if azure_coords:
        top_left_azure = min(azure_coords, key=lambda t: (t[0], t[1]))
        outline = trace_outline(input_grid, top_left_azure)

        if outline:
            # Bounding Box
            min_row = min(outline, key=lambda t: t[0])[0]
            max_row = max(outline, key=lambda t: t[0])[0]
            min_col = min(outline, key=lambda t: t[1])[1]
            max_col = max(outline, key=lambda t: t[1])[1]

            # Scale and map to inner 4x4
            for r, c in outline:
                out_r = int((r - min_row) * 3 / (max_row - min_row if max_row - min_row > 0 else 1)) + 1
                out_c = int((c - min_col) * 3 / (max_col - min_col if max_col - min_col > 0 else 1)) + 1
                if 1 <= out_r <= 4 and 1 <= out_c <=4: # ensure within bounds
                  output_grid[out_r, out_c] = 8

    return output_grid