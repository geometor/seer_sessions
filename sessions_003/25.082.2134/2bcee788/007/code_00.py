"""
1.  **Background Transformation:** Change all pixels of the initial background color (0) to color 3 (green).

2.  **Shape Identification:** Identify all contiguous shapes (orthogonally connected pixels of the same color) in the input grid. Do *not* change any pixel values yet.

3. **Target shape selection:**
    *   If color 6 is present, then do nothing to shape 6
    *   If color 2 is present, the shape that contains it is the "target shape"
    *   If only color 2 is not present, the "target shape" is defined by the shape with color 4, 7, or 8 (in order of example occurrence).

4.  **Target Shape Expansion:** Expand the target shape by one pixel in all four orthogonal directions (up, down, left, and right) *only if* the target pixel for expansion was originally the background color (0) in the input grid.

5.  **Other Shape Color Change:**
    *   In example 1, the non-target shape has color 2, and it is transformed to color 6.
    *    In example 4, the non-target shape has color 2 and is transformed to color 8.

6.  **Combined Color Change and Target Expansion:**
    *   If the "target" shape contains the color 2, it should be expanded to the background, and the expanded pixels should be of the "other shape color change", from step 5, that corresponds to the example.
        *   Example 1: shape 4 expands, shape 2 becomes 6
        *   Example 2: shape 2 expands, shape 6 remains
        *   Example 3: shape 7 expands, shape 2 remains.
        *   Example 4: shape 8 expands, shape 2 becomes 6.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.full_like(input_grid, 3)
    rows, cols = input_grid.shape

    def get_neighbors(r, c):
        """Gets the orthogonal neighbors of a cell."""
        neighbors = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbors.append((nr, nc))
        return neighbors

    def find_shapes(grid):
        """Finds all contiguous shapes in the grid."""
        visited = set()
        shapes = []
        for r in range(rows):
            for c in range(cols):
                if grid[r, c] != 0 and (r, c) not in visited:
                    color = grid[r, c]
                    shape_pixels = []
                    stack = [(r, c)]
                    while stack:
                        cr, cc = stack.pop()
                        if (cr, cc) in visited:
                            continue
                        visited.add((cr, cc))
                        shape_pixels.append((cr, cc))
                        for nr, nc in get_neighbors(cr, cc):
                            if grid[nr, nc] == color:
                                stack.append((nr, nc))
                    shapes.append({'color': color, 'pixels': shape_pixels})
        return shapes

    # Shape Identification
    shapes = find_shapes(input_grid)

    # Target shape selection
    target_shape = None
    other_shape_color_change = None

    for shape in shapes:
      if shape['color'] == 6:
          continue # skip shape with color 6
      if shape['color'] == 2:
          target_shape = shape
          break # first shape

    # handle case where there are no shapes of color 2
    if target_shape is None:
        for shape in shapes:
            if shape['color'] in [4, 7, 8]:
                target_shape = shape
                break

    # determine the other shape change
    if target_shape:
        if target_shape['color'] == 4:
            other_shape_color_change = 6
        elif target_shape['color'] == 8:
            other_shape_color_change = 6 # color 2 to 6
        elif any(shape['color'] == 4 for shape in shapes): # color 2
           other_shape_color_change = 6
        elif any(shape['color'] == 8 for shape in shapes):
            other_shape_color_change = 6


    for shape in shapes:
        if shape is target_shape:
            # Expansion of target shape
            expansion_color = shape['color']

            # check if color is 2 to overide expansion
            if shape['color'] == 2 and other_shape_color_change:
                expansion_color = other_shape_color_change

            for r, c in shape['pixels']:
              output_grid[r,c] = expansion_color # first fill the target
              for nr, nc in get_neighbors(r, c):
                  if input_grid[nr, nc] == 0:
                      output_grid[nr, nc] = expansion_color

        else: # Other shapes
            new_color = shape['color']

            # change other shape color, if needed
            if shape['color'] == 2 and other_shape_color_change is not None :
                new_color = other_shape_color_change

            for r, c in shape['pixels']:
                output_grid[r, c] = new_color


    return output_grid