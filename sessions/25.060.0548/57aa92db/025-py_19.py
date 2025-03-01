"""
1. Copy Azure: Copy all azure (8) colored objects from the input to the output grid without modification.
2. Expand Yellow: Locate the yellow (4) colored object. Extend this object downwards by two additional rows, replacing any red (2) pixels in those new positions with yellow (4).
3. Extend Green: Locate the green (3) colored object. If there is no azure object to the southeast of this, extend the green object along a line towards the southeast, adding green pixels to the output grid. If there *is* an azure object in the way, do not extend.
"""

import numpy as np

def find_objects_by_color(grid, color):
    """Finds all objects of a specific color in the grid."""
    objects = []
    rows, cols = grid.shape
    visited = set()

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and (r, c) not in visited:
                object_pixels = []
                queue = [(r, c)]
                visited.add((r, c))

                while queue:
                    curr_r, curr_c = queue.pop(0)
                    object_pixels.append((curr_r, curr_c))

                    # Check adjacent cells (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        new_r, new_c = curr_r + dr, curr_c + dc
                        if (0 <= new_r < rows and 0 <= new_c < cols and
                            grid[new_r, new_c] == color and (new_r, new_c) not in visited):
                            queue.append((new_r, new_c))
                            visited.add((new_r, new_c))

                objects.append(object_pixels)
    return objects

def is_blocked(grid, start_r, start_c, color_to_check):
    """Checks if there's an object of the specified color blocking southeast extension."""
    rows, cols = grid.shape
    r, c = start_r, start_c

    while 0 <= r < rows and 0 <= c < cols:
        if grid[r,c] == color_to_check:
          return True
        r += 1
        c += 1
    return False

def transform(input_grid):
    """Transforms the input grid according to the specified rules."""
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 1. Copy Azure
    #   (Already done by copying the input grid)

    # 2. Expand Yellow
    yellow_objects = find_objects_by_color(input_grid, 4)
    for obj in yellow_objects:
        # Find the bottom-most row of the object
        bottom_row = max(r for r, _ in obj)
        # Extend down by two rows, replacing 2s with 4s
        for r in range(bottom_row + 1, min(bottom_row + 3, rows)):
            for c in [c for _, c in obj]:  # Iterate over columns in the object
                if 0 <= r < rows and 0 <= c < cols: # bounds check
                    if output_grid[r,c] == 2:
                        output_grid[r, c] = 4
                    else:
                        output_grid[r,c] = 4


    # 3. Extend Green
    green_objects = find_objects_by_color(input_grid, 3)
    for obj in green_objects:
      start_r, start_c = obj[0]  # green object is always one pixel.
      if not is_blocked(input_grid, start_r, start_c, 8):
        r, c = start_r, start_c
        while 0 <= r < rows and 0 <= c < cols:
            output_grid[r,c] = 3
            r += 1
            c += 1

    return output_grid