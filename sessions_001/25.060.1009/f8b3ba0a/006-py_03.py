"""
1.  **Identify Colored Regions:** Examine the input grid to find all distinct, contiguous regions of non-zero pixels (objects). Pixels connected only diagonally are *not* considered part of the same region.

2.  **Locate Target Colors**: Within the identified objects, locate instances of yellow (4), red (2), and green (3). Note the color and the coordinates of the topmost, leftmost pixel of each of these colored objects.

3. **Determine Output Size and Content**:
    *   If the input grid contains a vertical line of yellow (4), red (2), and green (3) pixels in that order from top to bottom, create an output grid that has height equal to the number of colors, and width equal to the input. Fill each row of the output with the color and pad the rest with 0.
    *   Otherwise, create a grid with height equal to the number of colors and 1 column. Fill each cell with the color.

4.  **Order and Populate Output:** Arrange the found colors based on the row number of their topmost-leftmost pixel (ascending order). Populate the output grid based on derived logic.
"""

import numpy as np

def find_objects(grid):
    """
    Finds distinct colored regions (objects) in the grid.
    """
    objects = []
    visited = set()
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, color, current_object):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] != color:
            return
        visited.add((r, c))
        current_object.append((r, c))
        # Explore adjacent cells (not diagonally)
        dfs(r + 1, c, color, current_object)
        dfs(r - 1, c, color, current_object)
        dfs(r, c + 1, color, current_object)
        dfs(r, c - 1, color, current_object)

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited and grid[r, c] != 0:
                current_object = []
                dfs(r, c, grid[r, c], current_object)
                objects.append((grid[r,c],current_object)) # Store color and the object
    return objects

def check_vertical_stack(grid, target_colors):
    """
    Checks if the grid contains a vertical stack of the target colors.
    """
    rows, cols = grid.shape
    for c in range(cols):
        stack_colors = []
        for r in range(rows):
            if grid[r,c] in target_colors:
                stack_colors.append(grid[r,c])
        if len(stack_colors) >= len(target_colors):
             # check order
             match = True
             for i in range(len(target_colors)):
                if len(stack_colors) > i and stack_colors[i] != target_colors[i]:
                    match = False
             if match: return True
    return False


def transform(input_grid):
    """
    Transforms the input grid according to the defined rules.
    """
    input_grid_np = np.array(input_grid)
    # Find distinct colored regions
    objects = find_objects(input_grid_np)

    # Extract specific colors and their row order
    target_colors = [4, 2, 3]  # Yellow, Red, Green
    found_colors = []

    for color, obj_pixels in objects:
        if color in target_colors:
            topmost_row = min(pixel[0] for pixel in obj_pixels)
            found_colors.append((topmost_row, color))

    # sort the colors by row
    found_colors.sort()
    ordered_colors = [color for row, color in found_colors]

    # Determine output size
    if check_vertical_stack(input_grid_np, target_colors):
        output_grid = np.zeros((len(ordered_colors), input_grid_np.shape[1]), dtype=int)
        for i, color in enumerate(ordered_colors):
            output_grid[i, :] = color  # Fill entire row
    else:
      output_grid = np.zeros((len(ordered_colors), 1), dtype=int)
      for i in range(len(ordered_colors)):
          output_grid[i,0] = ordered_colors[i]

    return output_grid.tolist()