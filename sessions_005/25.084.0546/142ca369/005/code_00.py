"""
1.  **Identify Objects:** Find all contiguous blocks of non-zero colored pixels. Each block is an object.
2.  **Object Pairing and Connection:** Objects of different colors will attempt to connect diagonally based on these rules:
    *   Objects are considered for connection if they are within reasonable proximity. Objects far apart will not connect.
    *   Objects that *can* connect diagonally *will* connect diagonally. If a direct diagonal connection would pass through another object, the connection is not made.
    *   Objects that have multiple potential connections will connect to all valid partners.
    * Connections use a fill width that expands to the narrowest dimension of the two connecting objects, centered.

3. **Drawing Connections**
   * From the center of the first object, move diagonally towards the center of its connecting partner.
   * Connect to the center of the other object.
   * Expand the connection line to match the width of the *narrowest* of the two connecting objects. If one of the objects has a width of 1, the connection remains 1 pixel wide.
   * If more than one object shares the narrowest width, and they are both connecting to a larger object, use the combined width.
   * Fill all pixels between the two centers, not just a single diagonal line

"""

import numpy as np
from collections import deque

def find_objects(grid):
    """Finds all contiguous objects in a grid."""
    objects = []
    visited = set()
    rows, cols = grid.shape

    def _bfs(r, c, color):
        obj = []
        queue = deque([(r, c)])
        visited.add((r, c))

        while queue:
            row, col = queue.popleft()
            obj.append((row, col))

            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0), (1,1), (-1,-1), (1, -1), (-1, 1)]:
                nr, nc = row + dr, col + dc
                if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited and grid[nr, nc] == color:
                    queue.append((nr, nc))
                    visited.add((nr, nc))
        return obj

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and (r, c) not in visited:
                obj = _bfs(r, c, grid[r, c])
                objects.append((grid[r,c], obj))
    return objects

def get_object_bounds(obj):
    min_r, min_c = float('inf'), float('inf')
    max_r, max_c = float('-inf'), float('-inf')
    for r,c in obj:
        min_r = min(min_r, r)
        min_c = min(min_c, c)
        max_r = max(max_r, r)
        max_c = max(max_c, c)
    return min_r, min_c, max_r, max_c

def get_object_center(obj):
    min_r, min_c, max_r, max_c = get_object_bounds(obj)
    center_r = (min_r + max_r) // 2
    center_c = (min_c + max_c) // 2
    return center_r, center_c

def object_dimensions(obj):
    min_r, min_c, max_r, max_c = get_object_bounds(obj)
    return max_r - min_r + 1, max_c - min_c + 1

def object_distance(obj1, obj2):
    center1_r, center1_c = get_object_center(obj1)
    center2_r, center2_c = get_object_center(obj2)
    return abs(center1_r - center2_r) + abs(center1_c - center2_c)

def can_connect_diagonally(grid, obj1, obj2):
    """Checks if two objects can be connected diagonally without passing through other objects."""
    center1_r, center1_c = get_object_center(obj1)
    center2_r, center2_c = get_object_center(obj2)

    dr = 1 if center2_r > center1_r else -1
    dc = 1 if center2_c > center1_c else -1

    curr_r, curr_c = center1_r, center1_c
    while (curr_r != center2_r) or (curr_c != center2_c):
        next_r = curr_r + dr if curr_r != center2_r else curr_r
        next_c = curr_c + dc if curr_c != center2_c else curr_c
        
        # Check all intermediate pixels, not just the next center
        if grid[next_r, next_c] != 0 and (next_r, next_c) not in obj1 and (next_r, next_c) not in obj2:

            for r,c in obj1:
                if (next_r,next_c) == (r,c):
                    continue
            for r,c in obj2:
                if (next_r,next_c) == (r,c):
                    continue

            return False # Path Blocked

        curr_r, curr_c = next_r, next_c

    return True


def find_connections(grid, objects):
    """Finds valid connections between objects."""
    connections = []
    for i in range(len(objects)):
        for j in range(i + 1, len(objects)):
            color1, obj1 = objects[i]
            color2, obj2 = objects[j]
            if color1 != color2:
                if object_distance(obj1,obj2) < 10: # proximity check
                    if can_connect_diagonally(grid, obj1, obj2):
                        connections.append((i, j))
    return connections

def draw_connection(grid, obj1, obj2, color):
    """Draws a diagonal connection between two objects, filling all pixels."""
    center1_r, center1_c = get_object_center(obj1)
    center2_r, center2_c = get_object_center(obj2)

    dr = 1 if center2_r > center1_r else -1
    dc = 1 if center2_c > center1_c else -1

    # Determine fill width
    height1, width1 = object_dimensions(obj1)
    height2, width2 = object_dimensions(obj2)
    fill_width = min(height1, width1, height2, width2)

    curr_r, curr_c = center1_r, center1_c

    # Bresenham's line algorithm (modified for thick diagonal lines)
    dx = abs(center2_c - center1_c)
    dy = abs(center2_r - center1_r)
    sx = 1 if center1_c < center2_c else -1
    sy = 1 if center1_r < center2_r else -1
    err = dx - dy

    while True:
        # Fill with width
        for i in range(-(fill_width // 2), (fill_width + 1) // 2):
            row = max(0, min(grid.shape[0] - 1, curr_r + i))
            col = max(0, min(grid.shape[1] - 1, curr_c))
            if grid[row, col] == 0 or (row,col) in obj1:
                grid[row, col] = color

            row = max(0, min(grid.shape[0] - 1, curr_r))
            col = max(0, min(grid.shape[1] - 1, curr_c + i))
            if grid[row,col] == 0 or (row,col) in obj1:
                grid[row, col] = color


        if curr_r == center2_r and curr_c == center2_c:
            break

        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            curr_c += sx
        if e2 < dx:
            err += dx
            curr_r += sy



def transform(input_grid):
    grid = np.array(input_grid)
    objects = find_objects(grid)
    connections = find_connections(grid, objects)

    for i, j in connections:
        color1, obj1 = objects[i]
        _, obj2 = objects[j]
        draw_connection(grid, obj1, obj2, color1)


    return grid.tolist()