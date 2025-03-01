"""
1.  **Identify** all green pixels (value 3) in the input grid.
2.  **Find** the two closest, unconnected green pixels, using Manhattan Distance (|row1-row2|+|col1-col2|).
3.  **Connect** any two, unconnected green pixels, using the following steps, repeated until they are considered "connected":
    *   Draw a line of green pixels between them, prioritizing horizontal and vertical steps.
    *   If a direct horizontal/vertical connection is not possible, use the minimal number of diagonal steps necessary to connect the two.
    *   Two green pixels are considered "connected" if the Manhattan distance between them is 1.
4. **Repeat** steps 2 and 3 until all green pixels form a single connected component. A component is a group of pixels where any two in the group can reached using only up, down, left, or right.
5. **Preserve** all other pixels.
"""

import numpy as np
from collections import deque

def find_green_pixels(grid):
    """Finds all green pixels in the grid."""
    green_pixels = []
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 3:
                green_pixels.append((r, c))
    return green_pixels

def manhattan_distance(p1, p2):
    """Calculates the Manhattan distance between two points."""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def is_connected(pixel1, pixel2, grid):
     """Checks if two pixels are connected (Manhattan distance = 1)."""
     if manhattan_distance(pixel1,pixel2) == 1 and grid[pixel2] == 3:
        return True
     return False

def get_neighbors(pixel, grid_shape):
     """get neighbors within bounds"""
     row,col = pixel
     rows,cols = grid_shape
     neighbors = []

     if row > 0:
          neighbors.append((row - 1, col))  # Up
     if row < rows - 1:
        neighbors.append((row + 1, col))  # Down
     if col > 0:
          neighbors.append((row, col - 1))  # Left
     if col < cols - 1:
          neighbors.append((row, col + 1))  # Right

     return neighbors

def are_all_connected(green_pixels, grid):
    """Checks if all green pixels are connected using BFS."""
    if not green_pixels:
        return True

    visited = set()
    queue = deque([green_pixels[0]])
    visited.add(green_pixels[0])
    count = 0

    while queue:
        curr = queue.popleft()
        count += 1
        for neighbor in get_neighbors(curr, grid.shape):
          if grid[neighbor] == 3 and neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return count == len(green_pixels)

def connect_pixels(grid, p1, p2):
    """Connects two pixels using horizontal/vertical steps, minimizing diagonals."""
    r1, c1 = p1
    r2, c2 = p2
    new_grid = grid.copy()

    r_diff = r2 - r1
    c_diff = c2 - c1

    #prioritize horizontal/vertical
    while r_diff != 0:
        new_grid[r1 + (1 if r_diff > 0 else -1), c1] = 3
        r1 += (1 if r_diff > 0 else -1)
        r_diff = r2 - r1
    while c_diff != 0:
        new_grid[r1, c1 + (1 if c_diff>0 else -1)] = 3
        c1 += (1 if c_diff > 0 else -1)
        c_diff = c2-c1

    return new_grid

def transform(input_grid):
    # initialize output_grid
    output_grid = input_grid.copy()

    # find green pixels
    green_pixels = find_green_pixels(output_grid)

    #connect all green pixels until all form 1 connected component
    while not are_all_connected(green_pixels, output_grid):
      min_dist = float('inf')
      closest_pair = (None,None)

      for i in range(len(green_pixels)):
          for j in range(i+1, len(green_pixels)):
              if not is_connected(green_pixels[i],green_pixels[j], output_grid):
                  dist = manhattan_distance(green_pixels[i], green_pixels[j])
                  if dist < min_dist:
                      min_dist = dist
                      closest_pair = (green_pixels[i], green_pixels[j])
      if closest_pair[0] is not None:
        output_grid = connect_pixels(output_grid, closest_pair[0], closest_pair[1])
        green_pixels = find_green_pixels(output_grid)  #update the pixel list.
      else:  #all other components are connected.
        break

    return output_grid