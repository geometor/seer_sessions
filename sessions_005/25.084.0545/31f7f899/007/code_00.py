"""
1.  **Find Azure Line:** Locate the longest vertical line of azure (color 8) pixels. This line serves as a reference.

2.  **Identify Objects:** Identify all contiguous regions (objects) of the same color (excluding azure) that are directly adjacent (horizontally or vertically) to the azure line.

3.  **Process Each Object:** For each identified object:
    *   Find the top and bottom rows, leftmost and rightmost columns.
    *   Determine the color of that object
    *   Change all pixel in the segment from leftmost to rightmost in the object's top row to the object's color.
    *   Change all pixel in the segment from leftmost to rightmost in the object's bottom row to the object's color.

4.  **Output:** Return the modified grid.
"""

import numpy as np

def find_azure_line(grid):
    """Finds the longest vertical line of azure (8) pixels."""
    azure_lines = []
    rows, cols = grid.shape
    for c in range(cols):
        current_line = []
        for r in range(rows):
            if grid[r, c] == 8:
                current_line.append((r, c))
            else:
                if len(current_line) > 0:
                    azure_lines.append(current_line)
                current_line = []
        if len(current_line) > 0:
            azure_lines.append(current_line)

    longest_line = max(azure_lines, key=len, default=[])
    return longest_line

def find_objects(grid, azure_line):
    """Identifies contiguous colored objects adjacent to the azure line."""
    rows, cols = grid.shape
    objects = []
    visited = set()
    azure_line_set = set(azure_line)

    def is_adjacent_to_azure_line(r, c):
        """Checks if a cell is adjacent to the azure line."""
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if (nr, nc) in azure_line_set:
                return True
        return False

    def dfs(r, c, color, current_object):
        """Performs Depth-First Search to find connected components."""
        if (r, c) in visited or not (0 <= r < rows and 0 <= c < cols) or grid[r, c] != color:
            return

        visited.add((r, c))
        current_object.append((r, c))

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            dfs(r + dr, c + dc, color, current_object)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 8 and (r, c) not in visited and is_adjacent_to_azure_line(r, c):
                color = grid[r, c]
                current_object = []
                dfs(r, c, color, current_object)
                if current_object:
                    objects.append(current_object)
    return objects

def get_object_color(grid, object):
    """get color of object"""
    r,c = object[0]
    return grid[r,c]


def transform(input_grid):
    # initialize output_grid
    grid = np.array(input_grid)
    output_grid = grid.copy()
    rows, cols = grid.shape

    # Find the azure line
    azure_line = find_azure_line(grid)

    # Find objects adjacent to the azure line
    objects = find_objects(grid, azure_line)

    # Process each object
    for obj in objects:
        # Find top/bottom rows and leftmost/rightmost columns
        top_row = min(pixel[0] for pixel in obj)
        bottom_row = max(pixel[0] for pixel in obj)
        leftmost_col = min(pixel[1] for pixel in obj)
        rightmost_col = max(pixel[1] for pixel in obj)

        # Determine object's color
        object_color = get_object_color(grid, obj)

        # Fill the top and bottom row segments
        for c in range(leftmost_col, rightmost_col + 1):
            output_grid[top_row, c] = object_color
            output_grid[bottom_row, c] = object_color

    return output_grid.tolist()