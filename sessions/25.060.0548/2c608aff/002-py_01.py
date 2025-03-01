"""
The transformation rule identifies isolated single-pixel objects in a grid and extends them horizontally towards adjacent non-background objects. An object is considered isolated if all its 8-connected neighbors are background pixels. The extension happens only horizontally.
"""

import numpy as np
from collections import Counter

def get_objects(grid):
    """
    Identifies contiguous blocks of same-colored pixels as objects.
    """
    objects = []
    visited = set()
    rows, cols = grid.shape

    def dfs(r, c, color, current_object):
        if (r, c) in visited or not (0 <= r < rows and 0 <= c < cols) or grid[r, c] != color:
            return
        visited.add((r, c))
        current_object.append((r, c))
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                dfs(r + dr, c + dc, color, current_object)

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited:
                current_object = []
                dfs(r, c, grid[r, c], current_object)
                if current_object:
                    objects.append((grid[r,c], current_object)) # Store color with object
    return objects

def get_background_color(grid, objects):
    """
    Determine the background color. It's the most frequent color.
    """
    all_colors = []
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            all_colors.append(grid[r,c])
    
    color_counts = Counter(all_colors)

    most_common_color = color_counts.most_common(1)[0][0]
    return most_common_color


def is_isolated(grid, pixel, background_color):
    """
    Checks if a single-pixel object is isolated (surrounded by background).
    """
    r, c = pixel
    rows, cols = grid.shape

    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] != background_color:
                return False, (nr, nc) # return coordinates of neighbor
    return True, None # no non-background neighbors


def transform(input_grid):
    """
    Transforms the input grid according to the rule.
    """
    grid = np.array(input_grid)  # Convert to NumPy array
    rows, cols = grid.shape
    output_grid = np.copy(grid)  # Initialize output grid

    objects = get_objects(grid)
    background_color = get_background_color(grid, objects)


    # Find and extend isolated single-pixel objects
    for color, obj_pixels in objects:
        if len(obj_pixels) == 1:
            pixel = obj_pixels[0]
            isolated, neighbor_coord = is_isolated(grid, pixel, background_color)
            if not isolated and neighbor_coord is not None:
                r,c = pixel
                nr, nc = neighbor_coord
                
                if nc > c:
                    # extend to the right
                    for i in range(c+1, nc):
                        output_grid[r, i] = grid[r,c]

                elif nc < c:
                    # extend to the left
                    for i in range(nc+1, c):
                         output_grid[r, i] = grid[r,c]


    return output_grid.tolist()