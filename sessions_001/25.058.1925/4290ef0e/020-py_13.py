"""
1.  **Frame the Output:** Create an output grid of the same dimensions as the input grid.
2.  **Border:** Add a one-pixel wide yellow border around the output grid.
3.  **Background:** Fill the remaining area inside the border with green.
4.  **Object Detection:** Identify distinct contiguous regions (objects) of the same color within the input grid, *excluding* the green background.
5.  **Neighbor Check and Combination:**
    *   If an object has neighboring pixels of a *different* color (including diagonals), combine it with all its different-colored neighbors into a single, combined object.
    * If not continue to the next step with the single object.
6.  **Bounding Box:** Calculate the bounding box that encompasses the combined object (or the single object if no neighbors of different colors exist).
7.  **Draw:**
    *   Draw the bounding box in the output grid, filled with the color of the original, uncombined object's center pixel.
        The position of this box in output is the same as the input.
"""

import numpy as np

def find_objects(grid, background_color=3):
    """Finds contiguous objects of the same color, excluding the background."""
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    def dfs(row, col, color, obj_pixels):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        obj_pixels.append((row, col))
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                dfs(row + dr, col + dc, color, obj_pixels)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col] and grid[row, col] != background_color:
                object_pixels = []
                dfs(row, col, grid[row, col], object_pixels)
                objects.append(object_pixels)
    return objects

def get_neighbors(grid, object_pixels):
    """Finds all neighbors of an object including diagonal pixels"""
    neighbors = set()
    for r,c in object_pixels:
      for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
          if dr == 0 and dc == 0:
            continue
          nr, nc = r + dr, c + dc
          if 0 <= nr < grid.shape[0] and 0 <= nc < grid.shape[1]:
            neighbors.add( (nr,nc) )
    return list(neighbors)

def combine_objects(grid, object_pixels):
    """Combines an object with its differently colored neighbors."""
    combined_pixels = set(object_pixels)
    neighbors = get_neighbors(grid, object_pixels)
    object_color = grid[object_pixels[0]]

    for r, c in neighbors:
        if grid[r, c] != object_color:
          neighbor_object = find_object_at(grid, r, c)
          combined_pixels.update(neighbor_object)
    return list(combined_pixels)

def find_object_at(grid, row, col):
  """ locate object at specific point """
  for obj in find_objects(grid):
    if (row,col) in obj:
      return obj
  return []

def bounding_box(pixels):
    """Calculates the bounding box of a set of pixels."""
    if not pixels:
        return 0, 0, 0, 0  # Handle empty pixel list
    rows, cols = zip(*pixels)
    return min(rows), max(rows), min(cols), max(cols)

def get_object_center(object_pixels):
    """ approximate center of the shape """
    rows, cols = zip(*object_pixels)
    center_row = int(np.mean(rows) )
    center_col = int(np.mean(cols))
    return (center_row, center_col)

def transform(input_grid):
    # initialize output_grid - same dimensions as input
    input_grid = np.array(input_grid)
    output_grid = np.full_like(input_grid, 3)  # Initialize with green background

    # Frame with Yellow
    output_grid[0, :] = 4
    output_grid[-1, :] = 4
    output_grid[:, 0] = 4
    output_grid[:, -1] = 4

    # Find objects
    objects = find_objects(input_grid)

    # combine and draw boxes
    for obj in objects:
        # combine objects
        if has_different_neighbor(input_grid, obj):
          combined = combine_objects(input_grid, obj)
        else:
          combined = obj

        # bounding box
        min_row, max_row, min_col, max_col = bounding_box(combined)
        center_row, center_col = get_object_center(obj)
        color = input_grid[center_row,center_col]

        # draw to output
        output_grid[min_row:max_row+1, min_col:max_col+1] = color

    return output_grid.tolist()

def has_different_neighbor(grid, object_pixels):
    """Checks if an object has any neighbors of a different color."""
    object_color = grid[object_pixels[0]] # all pixels in object are the same color
    neighbors = get_neighbors(grid, object_pixels)
    for r, c in neighbors:
        if grid[r, c] != object_color:
            return True
    return False