"""
1.  **Find Top Boundary:** Locate the topmost horizontal line consisting entirely of gray (5) pixels. Record its row index.

2.  **Find Bottom Boundaries:** For each column, find the row index of the highest gray (5) pixel that is *below* the top boundary. If a column has *no* gray pixel below the top boundary, the bottom boundary for that column is the row immediately below the top boundary.

3.  **Identify Objects:** Scan the grid between the top and bottom boundaries (exclusive of the boundary rows themselves). Identify "objects," which are contiguous groups of pixels of the same color, *excluding* white (0) and gray (5). Contiguous means adjacent horizontally, vertically, *or diagonally*.

4. **Shift Objects Left:**
   *   Iterate through all identified objects.
   *   For *each* object:
       *  Determine the leftmost available column within the object's *current* row. A column is "available" if it is within the boundaries for that column and contains a white (0) pixel.
       * Move all pixels of the object to the leftmost available columns, maintaining the object's shape relative to its leftmost pixel, stopping when the object's pixels encounter any gray boundary pixel (left or vertical) or another object's pixel, defined as a non-white, non-gray pixel.

5. **Output:** The result is the modified grid after all objects have been shifted.
"""

import numpy as np

def find_top_boundary(grid):
    """Finds the row index of the top horizontal gray line."""
    for i, row in enumerate(grid):
        if all(pixel == 5 for pixel in row):
            return i
    return -1  # Should not happen in valid input

def find_bottom_boundaries(grid, top_row):
    """Finds the bottom boundary row for each column."""
    rows, cols = grid.shape
    bottom_boundaries = [-1] * cols

    for c in range(cols):
        for r in range(rows - 1, top_row, -1):
            if grid[r, c] == 5:
                bottom_boundaries[c] = r
                break
        if bottom_boundaries[c] == -1:
            bottom_boundaries[c] = top_row + 1

    return bottom_boundaries

def find_objects(grid, top_boundary, bottom_boundaries):
    """Identifies all objects within the specified boundaries."""
    rows, cols = grid.shape
    visited = set()
    objects = []

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, color, object_pixels):
        stack = [(r, c)]
        while stack:
            curr_r, curr_c = stack.pop()
            if (curr_r, curr_c) in visited:
                continue
            visited.add((curr_r, curr_c))

            if (curr_r > top_boundary and curr_r < bottom_boundaries[curr_c] and
                grid[curr_r, curr_c] == color):

                object_pixels.append((curr_r, curr_c))

                # Check all 8 neighbors
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = curr_r + dr, curr_c + dc
                        if is_valid(nr, nc):
                            stack.append((nr, nc))

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited and grid[r, c] != 0 and grid[r, c] != 5:
                if r > top_boundary and r < bottom_boundaries[c]:
                  object_pixels = []
                  dfs(r, c, grid[r, c], object_pixels)
                  if object_pixels:
                      objects.append({'color': grid[r, c], 'pixels': object_pixels})
    return objects

def shift_object_left(grid, object_pixels, top_boundary, bottom_boundaries):
  """Shifts a single object left within the boundaries."""
  output_grid = np.copy(grid)  # Work on a copy to avoid modifying original during iteration

  # Find the leftmost pixel's column in the object
  leftmost_col = min(c for _, c in object_pixels)
  color = grid[object_pixels[0][0],object_pixels[0][1]] #get color from first pixel

  # clear pixels
  for r, c in object_pixels:
      output_grid[r,c]=0

  # Determine the target leftmost column
  target_col = leftmost_col
  for c in range(leftmost_col -1, -1, -1):
    valid_move = True
    for r, _ in object_pixels:
        if not( r > top_boundary and r < bottom_boundaries[c] and output_grid[r,c] == 0):
          valid_move = False
          break
    if valid_move:
      target_col = c
    else:
      break

  # Shift the object to the new position
  for r, c in object_pixels:

      new_c = target_col + (c - leftmost_col)
      output_grid[r, new_c] = color


  return output_grid

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 1. Find Top Boundary
    top_boundary = find_top_boundary(input_grid)

    # 2. Find Bottom Boundaries
    bottom_boundaries = find_bottom_boundaries(input_grid, top_boundary)

    # 3. Identify Objects
    objects = find_objects(input_grid, top_boundary, bottom_boundaries)

    # 4. Shift Objects Left
    for obj in objects:
        output_grid = shift_object_left(output_grid, obj['pixels'], top_boundary, bottom_boundaries)

    # 5. Output
    return output_grid